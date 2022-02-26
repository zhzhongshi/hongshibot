# 事件处理必需依赖
from nonebot import on_command
from nonebot.adapters import Bot, Event
from nonebot.adapters.onebot.v11 import Bot,Message,GroupMessageEvent, MessageSegment
from nonebot.params import State
from nonebot.typing import T_State
# 数据来源
from . import data_source

qqmusic = on_command("点歌",aliases={"来首"}, priority=5)

@qqmusic.handle()
async def handle(bot: Bot, event: GroupMessageEvent,state: T_State=State()):
    args = str(event.get_message()).strip()
    msg = ''  
    if args !='':
        id =await data_source.qq_search(args)
        if id != '':
            msg=MessageSegment.music(type_='qq',id_=id)
    Msg = Message(msg)
    await qqmusic.finish(Msg)