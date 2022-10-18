import os
from pathlib import PurePath, Path
import  pandas as pd
import requests

# F:\wp_copy\农产品
filepath = PurePath(Path('F://wp_copy'), Path('农产品'))
os.chdir(filepath)

# url = http://aboc.agri.cn/brand/listByArea?areaId=100000&type=1
url = 'http://aboc.agri.cn/brand/listByArea?areaId=100000&type=1'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.35'
}

# 获取返回数据, json各市
response = requests.get(url, headers=headers)
prov_data= response.json()

# 遍历
# http://aboc.agri.cn/images/image/1572403908/65539b92ce8e4a8c99e8724ca81635a5.jpeg
brand_list = [
    {
        'brand_id':each_dict['id'],
        'brandType':each_dict['brandType'],
        'name':each_dict['name'],
        'origin':each_dict['origin'],
        'areaId': each_dict['areaId'],
        'img':'http://aboc.agri.cn/images' + each_dict['img'],
        'quyuType':each_dict['quyuType'],
        'categoryId':each_dict['categoryId'],
        'label':each_dict['label'],
        'intro':each_dict['intro'],
        'permitnumber':each_dict['permitnumber']
    }
    for each_dict in prov_data if each_dict['origin']
]

# 导出
brand_df = pd.DataFrame(brand_list)
brand_df.to_excel('out1.xlsx', index=False)

