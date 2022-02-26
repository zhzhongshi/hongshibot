from nonebot import on_command
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot.adapters.onebot.v11.message import Message
from nonebot.adapters.onebot.v11.event import  MessageEvent
from nonebot.typing import T_State
from nonebot.params import State, CommandArg
from .data_sources import encode,decode

#按照XZhouQD/nonebot-plugin-help要求的帮助及用法
# 若此文本不存在，将显示包的__doc__
__help_plugin_name__ = "encode" 
__des__ = '一个简单的加密解密'
__cmd__ = '''
加密：加密 原文
解密：解密 密文
'''.strip()
# __short_cmd__ = 'md2pic,text2pic'
__example__ = '''
加密 123
> #一串字母数字
解密 #一串字母数字
> 原文
'''.strip()

__usage__ = f'{__des__}\nUsage:\n{__cmd__}\n\nExample:\n{__example__}'


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
