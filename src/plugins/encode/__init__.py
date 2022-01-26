from nonebot import on_command
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot.adapters.onebot.v11.message import Message
from nonebot.adapters.onebot.v11.event import  MessageEvent
from nonebot.typing import T_State
from nonebot.params import State, CommandArg
from .data_sources import encode,decode

strencode = on_command("加密", priority=7)
@strencode.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State = State(), arg: Message=CommandArg()):
    arg = arg.extract_plain_text()
    print(arg)
    resp=await encode(arg)
    await strencode.finish(resp)
    
strdecode = on_command("解密", priority=7)
@strdecode.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State = State(), arg: Message=CommandArg()):
    arg = arg.extract_plain_text()
    print(arg)
    resp=await decode(arg)
    await strdecode.finish(str(resp).replace("&quot;","\""))
