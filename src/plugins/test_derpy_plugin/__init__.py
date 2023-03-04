from nonebot.plugin import PluginMetadata


__plugin_meta__ = PluginMetadata(
    name="呆站测试插件",
    description="破测试用的，小心使用哦！",
    usage='''
需要要“@”或叫名字
指令:
【查找图片】呆站/dp/derpy/derpibooru 编号
【随机 trending image】呆站热门/dptrending/dptrd
【反向搜索】呆站反搜/dpreverse/dprev
''',
    extra={
        "unique_name": "derpytest",
        "author": "Zerol Acqua <zerolacqua@outlook.com>",
        "version": "0.1.11",
    },
)

# 根据 ID 查找图片
from .functions import derpy
# 随机 trending image
from .functions import trend
# 反向搜图
from .functions import reverse

