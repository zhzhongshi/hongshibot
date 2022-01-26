#网易云、QQ音乐解析插件
import httpx
import json
import asyncio
from nonebot.log import logger
head={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Edg/92.0.902.78"}
async def neteasy_search(song_name:str) ->str:
    para={'s':song_name,'type':1}
    api='https://music.163.com/api/search/get/web'
    async with httpx.AsyncClient() as client:
        try:
            re=await client.get(url=api,params=para,headers=head)
        except:
            logger.error('music.163.com访问超时')
            logger.error('获取歌曲信息失败')
            return ''
    status=re.status_code
    if status!=200:
        return ''
    data=re.json()
    print(data)
    song_count=data['result']['songCount']
    if song_count==0:
        return ''
    
    songs=data['result']['songs']
    return str(songs[0]['id'])
async def qq_search(song_name:str) ->str:
    para={'w':song_name,'format':'json'}
    api='https://c.y.qq.com/soso/fcgi-bin/client_search_cp'
    async with httpx.AsyncClient() as client:
        try:
            re=await client.get(url=api,params=para,headers=head)
        except:
            logger.error('c.y.qq.com访问超时')
            logger.error('获取歌曲信息失败')
            return ''
    status=re.status_code
    if status!=200:
        return ''
    data=re.json()
    song_count=data['data']['song']['curnum']
    if song_count==0:
        return ''
    songs=data['data']['song']['list']
    return str(songs[0]['songid'])
