from nonebot import on_command
from nonebot.rule import to_me
from nonebot.permission import (
    SUPERUSER
)
from nonebot.matcher import Matcher
from nonebot.adapters.onebot.v11 import (
    Bot,
    Message,
    Event,
    GroupMessageEvent,
    GROUP_ADMIN,
    GROUP_OWNER
)
from nonebot.params import Arg, CommandArg, ArgPlainText, ArgParam


from .utils import (
    get_img_message_seg_by_ID,
    pick_rand_trend_message_seg,
    get_reverse_id_message
)

derpy = on_command("呆站", rule=to_me(), aliases={"dp","derpy", "derpibooru"}, priority=30,  block=True)

# @derpy.handle()
async def perssion_test(bot: Bot, event: GroupMessageEvent):
    if await SUPERUSER(bot, event):
        await derpy.send("识别到超级用户权限")
    elif await GROUP_ADMIN(bot, event):
        await derpy.send("识别到管理员权限")
    elif await GROUP_OWNER(bot, event):
        await derpy.send("识别到群主权限")
    else:
        # await derpy.finish("您没有权限（无慈悲）")
        await derpy.send("识别到普通权限")

@derpy.handle()
async def derpy_first_receive(matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text()  # 首次发送命令时跟随的参数，例：/呆站 1，则args为1
    if plain_text:
        matcher.set_arg("ID", args)  # 如果用户发送了参数则直接赋值

@derpy.got("ID", prompt="你没给咱 ID 呀？")
async def derpy_id(ID: Message = Arg(), ID_str: str = ArgPlainText("ID")):
    if not ID_str.isdigit():  # 如果参数不符合要求，则结束
        # 可以使用平台的 Message 类直接构造模板消息
        await derpy.finish(ID.template("说好了给 ID 的还不给，不管你了！"))
    derpy_image_message_seg = await get_img_message_seg_by_ID(ID_str)
    await derpy.finish(derpy_image_message_seg)


trend = on_command("呆站热门", rule=to_me(), aliases={"dptrending", "dptrd"}, priority=30, block=True)

@trend.handle()
async def trend_handle(bot: Bot, event: Event):
    rand_trend_message_seg = await pick_rand_trend_message_seg()
    await trend.finish(rand_trend_message_seg)


reverse = on_command("呆站反搜", rule=to_me(), aliases={"dpreverse", "dprev"}, priority=30, block=True)

@reverse.handle()
async def reverse_first_receive(matcher: Matcher, image_msg: Message = CommandArg()):
    image_seg_list = image_msg.get("image")  # 首次发送命令时跟随的参数，例：/呆站反搜 【图片】，则 image 为【图片】
    if len(image_seg_list)>0:
        matcher.set_arg("image", image_msg)

@reverse.got("image", prompt="得给咱图片吧？")
async def reverse_image(image_msg: Message = Arg("image")):
    print(Message)
    image_seg_list = image_msg.get("image")
    if len(image_seg_list)>0:
        img_url = image_seg_list[0].data.get("url", "")
        message = await get_reverse_id_message(img_url,distance=0.2)
        await reverse.finish(message)
    else:
        await reverse.finish(Message("哼，摆烂了！"))
