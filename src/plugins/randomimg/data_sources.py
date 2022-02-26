import asyncio
import httpx
from matplotlib.pyplot import table

url="https://iw233.cn/API/Random.php"
async def getImgUrl():
    async with httpx.AsyncClient() as client:
        returl=""
        resp = await client.get(url)
        if resp.is_redirect :
            returl=resp.headers.get("Location")
            return returl
