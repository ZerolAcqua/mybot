import requests

try:
    import ujson as json
except ModuleNotFoundError:
    import json

from nonebot.adapters.onebot.v11 import (
    MessageSegment,
    Message
)

# 由 GET 获取 API 数据，返回字典（由 json 数据转化）
def get_data_by_url(api_url: str)-> dict:
    req = requests.get(api_url)  # 请求连接
    if req.status_code==requests.codes.OK:
        return json.loads(req.text)
    else:
        return None

# 由 POST 获取 API 数据，返回字典（由 json 数据转化）
def post_data_by_url(api_url: str, data: dict)-> dict:
    req = requests.post(api_url,data= data)  # 请求连接
    if req.status_code==requests.codes.OK:
        return json.loads(req.text)
    else:
        return None

# 从图像 ID 获取 API 数据
def get_data_by_ID(ID: str)->str:
    api_url= 'https://trixiebooru.org/api/v1/json/images/'+ID
    return get_data_by_url(api_url)

# 从 API 字典数据获取单张图像的 url
def get_img_url(api_dict:dict,quality:str='medium')->str:
    if 'image' in api_dict:
        return api_dict['image']['representations'][quality]
    elif api_dict['images']==[]:
        return None
    else:
        return api_dict['images'][0]['representations'][quality]

# 从 API 字典数据获取单张图像的 ID
def get_img_ID(api_dict:dict)->str:
    if 'image' in api_dict:
        return str(api_dict['image']['id'])
    elif api_dict['images']==[]:
        return "N/A"
    else:
        return str(api_dict['images'][0]['id'])

# 单张图像的 tag 是否满足安全级 
def is_safe(api_dict:dict)->bool:
    if 'image' in api_dict:
        return "safe" in api_dict['image']['tags']
    elif api_dict['images']==[]:
        return None
    else:
        return "safe" in api_dict['images'][0]['tags'] 


# 在这里封装图像消息段
def get_img_message_seg(img_url: str)->MessageSegment:
    # return MessageSegment(type='image', data={'file':img_url})
    if img_url is None:
        return MessageSegment.text("没找到……")
    else: 
        return MessageSegment.image(img_url)

# 由呆站网址爬取图像，并生成消息段
async def get_img_message_seg_by_ID(ID: str)->MessageSegment:
    api_dict = get_data_by_ID(ID)
    if api_dict is None:
        return MessageSegment.text("（揉揉脑袋）好像出问题了！")
    if not is_safe(api_dict):
        # return MessageSegment(type='text', data={'text': "请您自己去找，不要坑我谢谢！"})
        return MessageSegment.text("请您自己去找，不要坑我谢谢！")
    img_url=get_img_url(api_dict)
    return get_img_message_seg(img_url)


import random
import time
from pathlib import Path

file_path = Path() / 'data' / 'derpy' / 'trendlist.json'
file_path.parent.mkdir(parents=True, exist_ok=True)
trendlist = (
    json.loads(file_path.read_text('utf-8'))
    if file_path.is_file()
    else {
        'date': time.strftime("%Y%m%d", time.localtime()), 
        'urls': []
    }
)

# 更新热门图像列表
def generate_trend_list()->None:
    if trendlist['date']!=time.strftime("%Y%m%d", time.localtime()) or trendlist['urls']==[]:
        get_trend_img_urls()
        save_blacklist()
    
# 获取热门图像url
def get_trend_img_urls(quality:str='medium')->None:
    trendlist['date']= time.strftime("%Y%m%d", time.localtime())
    trendlist['urls']= []
    api_dict=get_data_by_url('https://trixiebooru.org/api/v1/json/search/images?per_page=50&sd=desc&sf=wilson_score&q=safe%2Cfirst_seen_at.gt%3A3+days+ago')
    trendlist['urls']=[image['representations'][quality] for image in api_dict['images']]

# 保存为文件
def save_blacklist() -> None:
    file_path.write_text(json.dumps(trendlist), encoding='utf-8')

# 由随机抽取呆站热门图像，并生成消息段
async def pick_rand_trend_message_seg()->MessageSegment:
    generate_trend_list()
    img_url = random.choice(trendlist['urls'])
    return get_img_message_seg(img_url)

# 由图像反向搜索 ID ，并生成消息
async def get_reverse_id_message(img_url:str,distance=0.25)->Message:
    api_url= 'https://trixiebooru.org/api/v1/json/search/reverse'
    post_data = {
        'url': img_url,
        'distance': distance
    }
    api_dict= post_data_by_url(api_url, data=post_data)
    searched_img_url=get_img_url(api_dict)
    ID=get_img_ID(api_dict)
    if ID != "N/A":
        if not is_safe(api_dict):
            return MessageSegment.text("ID: "+ID+"\n") + MessageSegment.text("有什么不对劲！肯定是你的问题！")
        else:
            return MessageSegment.text("ID: "+ID+"\n") + get_img_message_seg(searched_img_url)
    else:
        return MessageSegment.text("咱……咱没找到呢……（小声）") 
