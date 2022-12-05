# from os import listdir
# from pc_honor import read_url

from time import strftime, localtime, time
from requests import get

#
# r = get('https://club.hihonor.com/cn/space-uid-7610984.html')
# print(r.status_code)
# print(r.encoding)


# 合并文件
# print(listdir('./data'))
# 读取url测试
# url_lists = read_url('./data/D1.csv', header=None)
# for i in range(len(url_lists)):
#     url = url_lists.pop()
#     print(f'第{i}个url -- {url}')
# print('总样本量: ', len(url_lists))

# # 日期
# d1 = strftime('%Y-%m-%d', localtime(time()))
# print(d1)

# for i, each in enumerate(['a', 'b'], start=1):
#     print(i, each)

from multiprocessing import Process


def f(name):
    print('hello', name)


if __name__ == '__main__':
    for i in range(5):
        print('=' * 100)
        print('i')
        p = Process(target=f, args=('bob',))
        p.start()
        p.join()
