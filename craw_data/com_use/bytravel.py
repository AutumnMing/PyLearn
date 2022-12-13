from parsel import Selector
from requests import get as requests_get


def crawl_url(area_url, encoding='gb2312'):
    r = requests_get(area_url)
    r.encoding = encoding
    if r.status_code == 200:
        return r.text


def parse_items(text, query_str):
    select = Selector(text)
    items = select.xpath(query_str)
    return items


# 解析返回 省级地址
def parse_prov(base_url, query_str, encoding='gb2312'):
    prov_text = crawl_url(base_url, encoding)
    items = parse_items(prov_text, query_str)
    for item in items:
        province = item.xpath('./a/text()').get().replace('特产', '')
        prov_url = base_url + item.xpath('./a/@href').get()
        if province not in ['香港', '澳门', '台湾']:
            yield province, prov_url


def parse_city(province, prov_url, query_str, encoding='gb2312'):
    # 获取 省下辖 -- 全体市信息 --
    text_city = crawl_url(prov_url, encoding)
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
        condition = '_list' in href or 'http' in href or '十大特产' in city or '十大特产' in district
        if not condition:
            yield {
                'province': province, 'city': city, 'district': district, 'href': href
            }


def parse_district(base_url, city_info, query_str, encoding='gb2312'):
    province, city = city_info.get('province'), city_info.get('city')
    # 无需解析, 直接是区县地址
    if city in ['北京', '上海', '重庆', '天津']:
        city_info['href'] = base_url + city_info.pop('href')
        yield city_info
    else:
        city_url = base_url + city_info.pop('href')
        text_district = crawl_url(city_url, encoding)
        items = parse_items(text_district, query_str)
        for item in items:
            district = item.xpath('./text()').get()
            href = item.xpath('./@href').get()
            condition1 = '_list' in href or 'http' in href
            condition2 = '十大特产' in district or '省' in district
            condition = condition1 or condition2
            if not condition:
                yield {
                    'province': province,
                    'city': city,
                    'district': district,
                    'href': base_url + href
                }


if __name__ == '__main__':

    url = 'http://shop.bytravel.cn'
    for province, prov_url in parse_prov(url, query_str='//div/div[@class="ht"]/b',encoding='gb2312'):
        for city_info in parse_city(province, prov_url, '//div[@class="ht"]/a', encoding='gb2312'):
            for d in parse_district(url, city_info, '//div[@class="ht"]/a'):
                print(d)
        print('='*150)
