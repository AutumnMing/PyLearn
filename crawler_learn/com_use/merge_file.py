import os
from pathlib import PurePath, Path
import pandas as pd

# 路径确认
filepath = PurePath(Path('F://wp_copy'), Path('农产品'), Path('Company'))
os.chdir(filepath)
# 读取数据
data_list = [ pd.read_csv(each, encoding='gb18030') for each in os.listdir() ]
data = pd.concat(data_list)
data['intro'] = data['intro'].str.strip()
data['url'] = 'http://aboc.agri.cn/images'
data['com_img'] = data['com_img'].fillna('')
data['com_img'] = data['url'].str.cat(data['com_img'])
data = data.drop(columns=['url'])

# 返回上级路径, 导出数据 + 'http://aboc.agri.cn/images' 图片前缀
os.chdir(filepath.parent)
data.to_csv('company.csv', encoding='utf-8', index=False)

