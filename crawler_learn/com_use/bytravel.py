
# 博雅特产网 ———— http://shop.bytravel.cn/
import requests


url = 'http://shop.bytravel.cn/'
r = requests.get(url)
print(r.encoding) # 原编码
r.encoding = 'gb2312' # 从网页elements看到网页编码
print(r.status_code)


print(r.text)