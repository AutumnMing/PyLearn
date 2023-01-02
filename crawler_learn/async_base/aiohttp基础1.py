import aiohttp
import asyncio


async def get(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            print("返回状态码:", response.status)
            html = await response.text()
            return html


async def request(url):
    print('正在访问链接: ', url)
    html = await get(url)
    print(html[:15])


if __name__ == '__main__':
    test_url = 'http://python.org'
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(get(test_url))
    # 显示调用的 get_event_loop方法在3.10版本后已经移除
    asyncio.run(get(test_url))
