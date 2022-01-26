from nonebot import on_command
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot.adapters.onebot.v11.message import Message,MessageSegment
from nonebot.adapters.onebot.v11.event import  MessageEvent
from nonebot.typing import T_State
from nonebot.params import State

import random

thisWaifuDoesNotExist = on_command("TWDNE",aliases={"该老婆不存在","thiswaifudoesnotexist","twdne"}, priority=5)
@thisWaifuDoesNotExist.handle()
async def _(bot: Bot):
    strrandint=str(random.randint(1,99999))
    print(strrandint)
    imgurl="https://www.thiswaifudoesnotexist.net/example-"+strrandint+".jpg"
    await thisWaifuDoesNotExist.send(MessageSegment(type='image', data={'file': imgurl}))