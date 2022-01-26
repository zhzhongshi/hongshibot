import asyncio
import time
import httpx

'''
POST /ajax/tools/ajax___secretcode.php HTTP/1.1
Content-Type: application/x-www-form-urlencoded
Host: www.mcmod.cn

type=code&text=text

HTTP/1.1 200

{"state":1,"result":"#ettpKvc"}
'''

url="https://www.mcmod.cn/ajax/tools/ajax___secretcode.php"
async def encode(text):
    async with httpx.AsyncClient() as client:
        data={'type':'code','text':text}
        resp = await client.post(url,data=data)
        result = resp.json()
        return result["result"]

async def decode(key):
    async with httpx.AsyncClient() as client:
        data={'type':'decode','key':key}
        resp = await client.post(url,data=data)
        result = resp.json()
        return result["result"]