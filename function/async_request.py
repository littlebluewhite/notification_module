import asyncio
import aiohttp
import requests


async def fetch(urls: list[str], headers: dict = None):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_data(session, url, headers) for url in urls]
        return await asyncio.gather(*tasks)


async def fetch_data(session, url, headers):
    async with session.get(url, headers=headers) as response:
        return await response.json()


def sync_fetch(urls: list[str]):
    result = []
    try:
        for url in urls:
            response = requests.get(url)
            response.raise_for_status()  # 檢查是否有 HTTP 錯誤發生
            response.json()
            result.append(response.json())  # 返回響應內容
    except requests.RequestException as e:
        return str(e)  # 返回錯誤信息
    return result
