"""
JRRP test plugin
Author: Zerol Acqua
Since: 30 Dec 2022
"""
# import random
# from datetime import date
# from nonebot import on_command
# from nonebot.rule import to_me
# from nonebot.plugin import PluginMetadata
# from nonebot.matcher import Matcher
# from nonebot.adapters import Message
# from nonebot.params import Arg, CommandArg, ArgPlainTex

import random
from datetime import date
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.plugin import PluginMetadata
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.adapters.onebot.v11.message import Message

__plugin_meta__ = PluginMetadata(
    name="今日人品测试插件",
    description="破测试用的",
    usage="指令：jrrp\n数值越低越好哦！",
    extra={
        "unique_name": "jrrptest",
        "author": "Zerol Acqua <zerolacqua@outlook.com>",
        "version": "0.1.0",
    },
)


def luck_simple(num):
    if num < 18:
        return '大吉'
    elif num < 53:
        return '吉'
    elif num < 58:
        return '半吉'
    elif num < 62:
        return '小吉'
    elif num < 65:
        return '末小吉'
    elif num < 71:
        return '末吉'
    else:
        return '凶'
    

jrrp = on_command("jrrp",rule=to_me(), aliases={"JRRP", "今日人品"}, priority=49, block=True)

@jrrp.handle()
async def jrrp_handle(bot: Bot, event: Event):
    rnd = random.Random()
    rnd.seed(int(date.today().strftime("%y%m%d")) + int(event.get_user_id()))
    lucknum = rnd.randint(1,100)
    await jrrp.finish(Message(f'[CQ:at,qq={event.get_user_id()}]您今日的幸运指数是{lucknum}/100，为"{luck_simple(lucknum)}"'))
