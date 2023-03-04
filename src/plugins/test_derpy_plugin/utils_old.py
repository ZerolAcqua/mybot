from bs4 import BeautifulSoup
from selenium import webdriver
from nonebot.adapters.onebot.v11 import (
    MessageSegment,
)

# 获取网页的 soup
def get_soup(url: str)-> BeautifulSoup:
    option = webdriver.ChromeOptions()
    option.add_argument('headless')  # 设置 option
    browser = webdriver.Chrome(options=option)
    browser.get(url)
    content = browser.page_source.encode('utf-8')
    browser.close()
    return BeautifulSoup(content, 'html.parser')

# 获取单张图像页面的图像 url
def get_img_url(soup:BeautifulSoup)->str:
    return soup.find('picture').find('img').attrs['src']

# 判断单张图像页面的 tag 是否满足安全级 
def is_safe(soup:BeautifulSoup)->bool:
    return soup.find(class_='tag dropdown').attrs['data-tag-name'] in ['safe']

# 在这里封装图像消息段
def get_img_message_seg(img_url: str)->MessageSegment:
    return MessageSegment(type='image', data={'file':img_url})

# 由呆站网址爬取图像，并生成消息段
async def pick_img_message_seg(url: str)->MessageSegment:
    # https://trixiebooru.org/images/id
    soup=get_soup(url)
    if not is_safe(soup):
        return MessageSegment(type='text', data={'text': "请您自己去找，不要坑我谢谢！"})
    img_url=get_img_url(soup)
    return get_img_message_seg(img_url)


import random
import time
from pathlib import Path
try:
    import ujson as json
except ModuleNotFoundError:
    import json

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
        pick_trend_img_urls()
        save_blacklist()
    
# 获取热门图像url
def pick_trend_img_urls()->None:
    trendlist['date']= time.strftime("%Y%m%d", time.localtime())
    trendlist['urls']= []
    for page in range(1,6):
        tar_url='https://trixiebooru.org/search?page={page}&sd=desc&sf=wilson_score&q=safe%2Cfirst_seen_at.gt%3A3+days+ago'
        soup=get_soup(tar_url)
        picture_list = soup.find_all('picture')
        temp_urls_list=[picture.find('img').attrs['src'].replace("thumb", "medium") for picture in picture_list]
        trendlist['urls'].extend(temp_urls_list)

# 保存为文件
def save_blacklist() -> None:
    file_path.write_text(json.dumps(trendlist), encoding='utf-8')

# 由随机抽取呆站热门图像，并生成消息段
async def pick_rand_trend_message_seg()->MessageSegment:
    generate_trend_list()
    img_url = random.choice(trendlist['urls'])
    return get_img_message_seg(img_url)
