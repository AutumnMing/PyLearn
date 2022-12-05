# 爬取地方人民政府的简介
import requests
from lxml import etree

url = 'http://www.luliang.gov.cn/zjll/theme.html'

r = requests.get(url)
tree = etree.HTML(r.text)
list_p = tree.xpath('//div[@class="xz_list"]//i/img/@src')
# for p in list_p:
#     print(p)

html_s = ';'.join(list_p)
print(html_s)