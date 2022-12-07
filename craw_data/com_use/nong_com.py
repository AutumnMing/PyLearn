import math
import os
from time import sleep
from pathlib import PurePath, Path
import pandas as pd
import numpy as np
import requests


filepath = PurePath(Path('F://wp_copy'), Path('农产品'), Path('Company'))
os.chdir(filepath)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 '
                  'Safari/537.36 Edg/107.0.1418.35 '
}

# # 采集全部省份信息的url
# url = "http://aboc.agri.cn/area/child?pid=100000"
# res1 = requests.get(url, headers=headers)
# prov_id_list = res1.json()
#
# # 省信息
# prov_info = [
#     {
#         'prov_id':prov_dict['id'],
#         'code':prov_dict['code'],
#         'province':prov_dict['qname'],
#         'prov_name':prov_dict['name'],
#         'pid':prov_dict['pid'],
#         'lv':prov_dict['lv']
#     }
#     for prov_dict in prov_id_list
# ]

# 总页码信息
# http://aboc.agri.cn/brand/list?type=2&areaId=&categoryId=&companyScala=&pageNumber=1&pageSize=12
url = 'http://aboc.agri.cn/brand/list?type=2&areaId=&categoryId=&companyScala='
params = {'pageNumber': 1, 'pageSize': 12}
res1 = requests.get(url, params=params)
res_dict = res1.json()
totalPages = res_dict['totalPages']

df_list = []
for page_num in np.arange(1, 1 + totalPages):
    # 获取单页信息
    print('正在获取信息, ', '页码为: ', page_num)
    params = {'pageNumber': page_num, 'pageSize': 12}
    res1 = requests.get(url, params=params)
    res_dict = res1.json()
    # 单页信息的获取,企业列表
    company_lists = res_dict['content']
    # 原始企业信息迭代查询
    # for com_dict in company_lists:
    #     print(com_dict)

    # 'http://aboc.agri.cn/images' 图片url
    com_list = [
        {
            'areaId': com_dict['areaId'],
            'areaName': com_dict['view']['areaName'],
            'company_id': com_dict['id'],
            'company_name': com_dict['name'],
            'headquarters': com_dict['headquarters'],
            'mainService': com_dict['mainService'],
            'com_img': com_dict['img'],
            'categoryId': com_dict['categoryId'],
            'parentCategoryId': com_dict['parentCategoryId'],
            'label': com_dict['label'],
            'intro': com_dict['intro']
        }
        for com_dict in company_lists
    ]

    # 数据转换为DataFrame并导出
    com_df = pd.DataFrame(com_list)
    df_list.append(com_df)
    sleep(0.1)

    # 结果导出, 每100页
    if page_num%10 == 0:
        filename = 'out' + str(int(page_num / 10)) + '.csv'
        pd.concat(df_list).to_csv(filename, index=False, encoding='gb18030')
        print('已经累计满10页数据, ', '导出到文件', filename)
        df_list.clear()
    if page_num == totalPages:
        filename = 'out' + str(math.ceil(page_num / 10)) + '.csv'
        pd.concat(df_list).to_csv(filename, index=False, encoding='gb18030')
        print('已到最后一页, ', '导出到文件', filename)
        df_list.clear()

