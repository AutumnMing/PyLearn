import asyncio


# 定义一个协程
async def execute(x):
    print('定义一个协程')
    print('Hello ...')
    await asyncio.sleep(1)
    print('... World!')
    print(x)


if __name__ == '__main__':
    # 直接运行协程函数, 函数没有执行, 返回的是协程对象
    a = execute(10)
    print(type(a))
    # run
    asyncio.run(execute(11))

