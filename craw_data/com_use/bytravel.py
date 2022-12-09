from parsel import Selector
from requests import get as requests_get


def crawl_url(area_url, encodings='gb2312'):
    r = requests_get(area_url)
    r.encoding = encodings
    if r.status_code == 200:
        return r.text


def parse_items(text, query_str):
    select = Selector(text)
    items = select.xpath(query_str)
    return items


def crawl_prov_url(prov_url, encodings='gb2312'):
    return crawl_url(prov_url, encodings)



def parse_prov(prov_text, query_str, base_url):
    # base_url = 'http://shop.bytravel.cn'
    items = parse_items(prov_text, query_str)
    for item in items:
        yield  {
            'province': item.xpath('./a/text()').get().replace('特产', ''),
            'href': base_url + item.xpath('./a/@href').get()
        }


def craw_city_url(city_url, encodings='gb2312'):
    return crawl_url(city_url, encodings)


# 返回城市级url信息 prov, city, city_url
def parse_city(text, query_str, province):
    items = parse_items(text, query_str)
    # 获取城市相关信息
    for item in items:
        yield {
            'province': province,
            'city': item.xpath('./text()').get(),
            'href': item.xpath('./@href').get()
        }



# 原位置更新 url 的信息
def clean_area(area_url, condition, base_url, key):
    if not condition:
        area_url[key] = base_url + area_url[key]
        return area_url


def clean_city(city_rul, base_url, key='href'):
    # 清除掉非城市的url
    condition = '_list' in city_rul['href'] or 'http' in city_rul['href'] or '十大特产' in city_rul['city']
    return clean_area(city_rul, condition, base_url, key=key)



if __name__ == '__main__':
    url = 'http://shop.bytravel.cn'
    pass
