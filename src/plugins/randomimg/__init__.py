from nonebot import on_command
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot.adapters.onebot.v11.message import MessageSegment
from nonebot.adapters.onebot.v11.event import  MessageEvent
from nonebot.typing import T_State
from nonebot.params import State
from .data_sources import getImgUrl

randomimg = on_command("图来",aliases={"随机一图","色图来"}, priority=9)
@randomimg.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State = State()):
    resp=await getImgUrl()
    await randomimg.send(str(resp))
    await randomimg.send(MessageSegment(type='image', data={'file': resp}))
