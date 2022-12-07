from time import sleep
from collections import deque
from parsel import Selector
from requests import get as requests_get




def crawl_url(url, encodings='gb2312'):
    r = requests_get(url)
    r.encoding = encodings
    if r.status_code == 200:
        return r.text


def parse_items(text, query_str):
    select = Selector(text)
    items = select.xpath(query_str)
    return items


def crawl_prov_url(url, encodings='gb2312'):
    return crawl_url(url, encodings)


def parse_prov(text, query_str, base_url):
    # base_url = 'http://shop.bytravel.cn'
    items = parse_items(text, query_str)
    prov_list = [
        {
            'province': item.xpath('./a/text()').get().replace('特产', ''),
            'href': base_url + item.xpath('./a/@href').get()
        }
        for item in items
    ]
    return prov_list


def craw_city_url(url, encodings='gb2312'):
    return crawl_url(url, encodings)


def parse_city(text, query_str, province):
    items = parse_items(text, query_str)
    # 获取城市相关信息
    city_list = [
        {
            'province': province,
            'city': item.xpath('./text()').get(),
            'href': item.xpath('./@href').get()
        }
        for item in items
    ]
    return  city_list


# 原位置更新 url 的信息
def clean_area(area, condition, base_url, key):
    if not condition:
        area[key] = base_url + area[key]
        return area




if __name__ == '__main__':

    url = 'http://shop.bytravel.cn'

    # step2: 通过省获取地级市的url
    # -- {'province': '江苏', 'href': 'http://shop.bytravel.cn/produce/index118.html'}
    url = 'http://shop.bytravel.cn/produce/index118.html'
    r = requests.get(url)
    r.encoding = 'gb2312'
    select = Selector(r.text)
    items = select.xpath('//div[@class="ht"]/a')

    # 获取城市相关信息
    city_list = [
        {
            'province': '江苏',
            'city': item.xpath('./text()').get(),
            'href': item.xpath('./@href').get()
        }
        for item in items
    ]
    # 清除掉非城市的url
    clean_city_list = []
    for each in city_list:
        condition = '_list' in each['href'] or 'http' in each['href'] or '十大特产' in each['city']
        if not condition:
            each['href'] = 'http://shop.bytravel.cn' + each['href']
            clean_city_list.append(each)

    # step3: {'province': '江苏', 'city': '苏州市', 'href': 'http://shop.bytravel.cn/produce/index203.html'}
    # 通过城市获取区县信息
    url = 'http://shop.bytravel.cn/produce/index203.html'
    r = requests.get(url)
    r.encoding = 'gb2312'
    select = Selector(r.text)
    items = select.xpath('//div[@class="ht"]/a')
