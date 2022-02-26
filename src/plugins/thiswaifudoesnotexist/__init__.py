from nonebot import on_command
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot.adapters.onebot.v11.message import Message,MessageSegment
from nonebot.adapters.onebot.v11.event import  MessageEvent
from nonebot.typing import T_State
from nonebot.params import State

import random

#按照XZhouQD/nonebot-plugin-help要求的帮助及用法
# 若此文本不存在，将显示包的__doc__
__help_plugin_name__ = "thiswaifudoesnotexist" 
__des__ = '该老婆不存在'
__cmd__ = '''
TWDNE
该老婆不存在
hiswaifudoesnotexist
twdne
'''.strip()
__example__ = '''
该老婆不存在
> [图片]
'''.strip()

__usage__ = f'{__des__}\nUsage:\n{__cmd__}\n\nExample:\n{__example__}'


thisWaifuDoesNotExist = on_command("TWDNE",aliases={"该老婆不存在","thiswaifudoesnotexist","twdne"}, priority=5)
@thisWaifuDoesNotExist.handle()
async def _(bot: Bot):
    strrandint=str(random.randint(1,99999))
    print(strrandint)
    imgurl="https://www.thiswaifudoesnotexist.net/example-"+strrandint+".jpg"
    await thisWaifuDoesNotExist.send(MessageSegment(type='image', data={'file': imgurl}))