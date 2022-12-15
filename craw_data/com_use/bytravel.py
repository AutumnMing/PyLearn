from time import sleep
from os.path import exists
from os import remove
from csv import DictWriter
from pathlib import PurePath, Path
from parsel import Selector
from requests import get as requests_get
from numpy.random import rand
from pandas import read_csv


def crawl_url(area_url: str, encoding: str = 'gb2312') -> str:
    """
    根据传入的url获取网页信息
    :param area_url: 采集的url地址
    :param encoding: 网站返回的文本编码
    :return: str
    """
    r = requests_get(area_url)
    r.encoding = encoding
    if r.status_code == 200:
        return r.text


def parse_items(text: str, query_str: str):
    """
    解析网页文本
    :param text: 网页文本
    :param query_str: xpath表达式
    :return: Selector对象
    """
    select = Selector(text)
    items = select.xpath(query_str)
    return items


# 解析返回 省级地址
def parse_prov(base_url: str, query_str: str, encoding: str = 'gb2312') -> dict:
    """
    解析省份信息
    :param base_url:
    :param query_str:
    :param encoding:
    :return: dict, 返回省份名称和url的字典
    """
    prov_text = crawl_url(base_url, encoding)
    items = parse_items(prov_text, query_str)
    for item in items:
        province = item.xpath('./a/text()').get().replace('特产', '')
        prov_url = base_url + item.xpath('./a/@href').get()
        if province not in ['香港', '澳门', '台湾']:
            yield {
                'province': province, 'href': prov_url
            }


def parse_city(prov_info, query_str, encoding='gb2312'):
    province, prov_url = prov_info.pop('province'), prov_info.pop('href')
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


def parse_district(city_info, query_str, encoding='gb2312'):
    province, city = city_info.get('province'), city_info.get('city')
    # 无需解析, 直接是区县地址
    if city in ['北京', '上海', '重庆', '天津']:
        yield city_info
    else:
        city_url = 'http://shop.bytravel.cn' + city_info.pop('href')
        text_district = crawl_url(city_url, encoding)
        items = parse_items(text_district, query_str)
        for item in items:
            district = item.xpath('./text()').get()
            href = item.xpath('./@href').get()
            # 地址清洗
            condition1 = '_list' in href or 'http' in href
            condition2 = '十大特产' in district or '省' in district
            condition3 = district == province
            condition = condition1 or condition2 or condition3
            if not condition:
                yield {
                    'province': province,
                    'city': city,
                    'district': district,
                    'href': href
                }


def to_csv(data, filename, fieldnames, mode, encoding='utf-8', filepath=None):
    if filepath:
        filename = PurePath(Path(filepath), Path(filename))
    # print(data)
    with open(filename, mode=mode, encoding=encoding, newline='') as f:
        writer = DictWriter(f, fieldnames)
        writer.writerow(data)


def get_all_district(base_url, filename, fieldnames, mode, filepath=None):
    generator = parse_prov(base_url, query_str='//div/div[@class="ht"]/b', encoding='gb2312')
    for each_prov in generator:
        sleep(0.1 + 0.1 * rand())
        # 采集城市信息
        for each_city in parse_city(each_prov, '//div[@class="ht"]/a', encoding='gb2312'):
            print('+' * 150)
            # 采集区县信息
            sleep(0.05 + 0.05 * rand())
            for each_district in parse_district(each_city, '//div[@class="ht"]/a', encoding='gb2312'):
                to_csv(each_district, filename, fieldnames, mode=mode, filepath=filepath)
                sleep(0.02 + 0.03 * rand())
        print('=' * 150)


def clean_district(filename, columns, filepath=None):
    # 读取csv文件, 添加列名
    if filepath:
        filename = PurePath(Path(filepath, Path(filename)))
    dft = read_csv(filename, header=None).drop_duplicates()
    dft.columns = columns
    return dft


def clean_district_url(filename, columns, url_type='phone', filepath=None, export_csv=False):
    # 读取csv文件, 添加列名 + 清洗url
    clean_file_name = 'clean_' + filename
    dft = clean_district(filename, columns, filepath)
    if url_type == 'phone':
        dft['href'] = 'http://m.bytravel.cn' + dft['href']
    if url_type == 'pc':
        dft['href'] = 'http://shop.bytravel.cn' + dft['href']
    if export_csv:
        clean_file_name = PurePath(Path(filepath, Path(clean_file_name)))
        dft.to_csv(clean_file_name, encoding='utf-8', index=False)
    return dft


def district_specialty(district_info, filename, fieldnames, mode, filepath=None):
    url = district_info.pop('href')
    text = crawl_url(url)
    items = parse_items(text, query_str='//ul[@id="titlename"]')
    sleep(0.1 + 0.1 * rand())
    print('==' * 70)
    print('采集区域', '-', 'province', district_info.get('province'), '-', 'city', district_info.get('city'), sep=' ')
    print('=+' * 70)
    for index, item in enumerate(items, start=1):
        specialty_name = item.xpath('./li/a/text()').get()  # 特产名称
        img = item.xpath('./li/a/img/@src').get()  # 是否地标
        # 特产详情页
        specialty_url = item.xpath('./li/a/@href').get()
        landmark = 0
        if isinstance(img, str):
            landmark = 1
        district_info['landmark'] = landmark
        district_info['specialty_name'] = specialty_name
        district_info['specialty_url'] = 'http://m.bytravel.cn' + specialty_url
        to_csv(district_info, filename, fieldnames, mode=mode, filepath=filepath)
        print(index, district_info, sep=' : ')
        sleep(0.1 + 0.1 * rand())
    print('==' * 70)
    print('\n')

    # df = read_csv('./data/ct_specialty.csv', header=None)
    # col_names = ['province', 'city', 'district', 'landmark', 'specialty_name', 'specialty_url']
    # df.columns = col_names
    # df['specialty_name'] = df['specialty_name'].str.replace(' ', '')
    # df.to_excel('./data/ct_specialty.xlsx', index=False)
    # print(df.loc[0:5,col_names[0:5]])

def clean_district_specialty(filename, columns, filepath=None, export_csv=False, export_xlsx=False):
    clean_file_name = 'clean_' + filename
    dft = clean_district(filename, columns, filepath)
    dft['specialty_name'] = dft['specialty_name'].str.replace(' ', '')
    if export_csv:
        clean_file_name = PurePath(Path(filepath, Path(clean_file_name)))
        dft.to_csv(clean_file_name, encoding='utf-8', index=False)
    if export_xlsx:
        clean_file_name = PurePath(Path(filepath, Path(clean_file_name.replace('csv', 'xlsx'))))
        dft.to_excel(clean_file_name, index=False)
    return dft


def check_file(filename, filepath=None):
    if filepath:
        print(f'文件存储路径为: {filepath}')
        filename = PurePath(Path(filepath), Path(filename))
    if exists(filename):
        print(f'目标文件已存在: {filename.parts[-1]}')
        remove(filename)


if __name__ == '__main__':

    # step1: -- 采集所有地区的url信息, 精确到区县
    check_file('district.csv', filepath='./data')

    url = 'http://shop.bytravel.cn'
    col_names = ['province', 'city', 'district', 'href']
    get_all_district(url, 'district.csv', col_names, mode='a+', filepath='./data')

    # step2: -- 清洗url
    col_names = ['province', 'city', 'district', 'href']
    df = clean_district_url('district.csv', col_names, url_type='phone', filepath='./data', export_csv=False)

    # step3: -- 采集特产数据
    check_file('ct_specialty.csv', filepath='./data')
    df = read_csv('./data/clean_district.csv')
    col_names = ['province', 'city', 'district', 'landmark', 'specialty_name', 'specialty_url']
    for each_district_info in df.to_dict('records'):
        district_specialty(each_district_info, 'ct_specialty.csv', fieldnames=col_names, mode='a+', filepath='./data')

    # step4: -- 清洗特产数据 --
    col_names = ['province', 'city', 'district', 'landmark', 'specialty_name', 'specialty_url']
    df = clean_district_specialty('ct_specialty.csv', col_names, filepath='./data', export_xlsx=True)
    print(df.loc[:,col_names[0:5]].head())
    pass