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


# 解析返回 省级地址
def parse_prov(prov_text, query_str, base_url):
    # base_url = 'http://shop.bytravel.cn'
    # 获取全部省份的 url 信息
    items = parse_items(prov_text, query_str)
    for item in items:
        province = item.xpath('./a/text()').get().replace('特产', '')
        prov_url = base_url + item.xpath('./a/@href').get()
        if province not in ['香港', '澳门', '台湾']:
            yield province, prov_url


# def clean_district(district_url, base_url, key='href'):
#     condition1 = '_list' in district_url['href'] or 'http' in district_url['href']
#     condition2 = '十大特产' in district_url['district'] or '省' in district_url['district']
#     condition = condition1 or condition2
#     return clean_area(district_url, condition, base_url, key)


# 返回城市级url信息 -- 用于清洗后解析区县
def parse_city(province, prov_url, query_str, encodings='gb2312'):
    # 获取 省下辖 -- 全体市信息 --
    text_city = crawl_url(prov_url, encodings)
    items = parse_items(text_city, query_str)
    # 获取省份下辖城市 -- 去除其他相关信息
    for item in items:
        # 断url获取
        href = item.xpath('./@href').get()
        if province in ['北京', '上海', '重庆', '天津']:
            # 这4个地区直接采集到了区县的url信息
            city = province
            district = item.xpath('./text()').get()
        else:
            city = item.xpath('./text()').get()
            district = ''
        # 数据清洗, 清洗掉十大特产, 等列表形式的url
        condition = '_list' in href or 'http' in href or '十大特产' in city
        if not condition:
            yield {
                'province': province, 'city': city, 'district': district, 'city_url': href
            }



def parse_district(city_info, query_str):

    items = parse_items(text_district, query_str)
    for item in items:
        yield {
            'province': province,
            'city': city,
            'district': item.xpath('./text()').get(),
            'href': item.xpath('./@href').get()
        }


# 测试clean_area功能的函数
def test_clean_area(area_url: dict, condition: bool, base_url: str, key_update: str):
    if not condition:
        area_url[key_update] = base_url + area_url[key_update]
        return area_url
    if condition:
        return None


if __name__ == '__main__':

    base_url = 'http://shop.bytravel.cn'
    query_strs = '//div/div[@class="ht"]/b'
    encoding = 'gb2312'
    prov_texts = crawl_prov_url(base_url, encoding)
    for province, prov_url in parse_prov(prov_texts, query_strs, base_url):
        print('='*150)
        city_texts = craw_city_url(prov_url, encoding)
        for city_url in parse_city(city_texts, '//div[@class="ht"]/a', province, base_url):
            print(city_url)
        print('='*150)

    # area_url = {'href':'/produce/food/index203_list.html'}
    # value1 = test_clean_area(area_url, condition=True, base_url=url, key_update='href')
    # print(value1)
    # value1 = test_clean_area(area_url, condition=False, base_url=url, key_update='href')
    # print(value1)
