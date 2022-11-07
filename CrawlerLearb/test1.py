import os
from pathlib import PurePath, Path

import numpy as np
import requests


filepath = PurePath(Path('F://wp_copy'), Path('农产品'), Path('Company'))
os.chdir(filepath)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 '
                  'Safari/537.36 Edg/107.0.1418.35 '
}

# 总页码信息
# http://aboc.agri.cn/brand/list?type=2&areaId=&categoryId=&companyScala=&pageNumber=1&pageSize=12
url = 'http://aboc.agri.cn/brand/list?type=2&areaId=&categoryId=&companyScala='
params = {'pageNumber': 1, 'pageSize': 12}
res1 = requests.get(url, params=params)
res_dict = res1.json()
totalPages = res_dict['totalPages']

df_list = []
for page_num in np.arange(1, 1 + 3):
    # 获取单页信息
    print('正在获取信息, ', '页码为: ', page_num)
    params = {'pageNumber': page_num, 'pageSize': 12}
    res1 = requests.get(url, params=params)
    res_dict = res1.json()
    # 单页信息的获取,企业列表
    company_lists = res_dict['content']

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

    for each in com_list:print(each)