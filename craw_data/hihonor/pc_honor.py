from time import sleep
from time import strftime, localtime, time
from collections import deque
import requests
from parsel import Selector
from numpy import arange
from numpy.random import rand
from pandas import DataFrame, read_csv


# 写入数据
def append_csv(dft, filename, encoding='utf-8'):
    dft.to_csv(filename, mode='a', encoding=encoding, header=False, index=False)


# 分块读取, 返回由 多个list 组成的列表
def read_url(filename, header: int | None, url_name='space_url', chunksize: int | None = None):
    if chunksize is None:
        return deque(read_csv(filename, header=header)[url_name].tolist())
    if chunksize:
        data = read_csv(filename, header=header, chunksize=chunksize)
        return [each.loc[:, url_name].tolist() for each in data]


def get_base_url(max_page: int, page_type: str | None):
    for page_num in arange(max_page, 0, -1):
        yield f'https://club.hihonor.com/cn/forum-{page_type}-{page_num}.html?filter=dateline'


# 抓取板块页面信息
def scrape_model_page(model_url, headers):
    try:
        r = requests.get(model_url, headers=headers)
        if r.status_code == 200:
            return r.text
    except requests.RequestException as e1:
        print(f'报错{e1}, 此刻的url为: {model_url}')


# 解析版块页面信息, 获取空间主页url, uid, 用户昵称
# https://club.hihonor.com/cn/space-uid-213949242.html, 空间url示例
def parse_model_page(text):
    selector = Selector(text)
    items = selector.xpath('//a[@class="avatar-name"]')
    space_urls = []
    print('本页采集数目: ', len(items))
    for item in items:
        short_href = item.xpath('./@href').get()  # 短链接
        space_url = {
            'uid': short_href.partition('space-uid-')[-1].replace('.html', ''),
            'user_name': item.xpath('./text()').get(),
            'url': 'https://club.hihonor.com/cn/' + short_href
        }
        space_urls.append(space_url)
    return DataFrame(space_urls)


# 代码功能整合 -- 采集用户的空间的url --
def get_space_urls(max_page, page_type, headers, filename):
    generator = get_base_url(max_page=max_page, page_type=page_type)
    while True:
        try:
            model_url = next(generator)
            text = scrape_model_page(model_url, headers)
            dft = parse_model_page(text)
            append_csv(dft, filename)
            sleep(0.05 + rand() * 0.35)
        except StopIteration:
            print('采集完成')
            break  # 终止循环, 避免死循环


# 抓取用户的空间详细信息
def scrape_space(space_url, headers):
    sleep(rand() * 0.1)
    return scrape_model_page(space_url, headers)


# 解析用户空间详细信息
def parse_space_info(text):
    selector = Selector(text)
    user_name = selector.xpath('//div[@class="pc-brief"]/h1/text()').get()  # 用户昵称
    user_lv = selector.xpath('//div[@class="pc-brief"]/p/text()').get()  # 用户等级
    province = selector.xpath('//div[@class="pc-brief"]/p/span/text()').get()  # 所在省份
    post_num = selector.xpath('//ul[@class="pcb-sum"]/li/span/text()').get()  # 发帖数量
    uid = selector.xpath('//tbody/tr[1]/td/text()').get()  # uid
    friends = selector.xpath('//tbody/tr[3]/td/text()').get()  # 好友数
    total_sign = selector.xpath('//tbody/tr[4]/td/p[1]/b/text()').get()  # 累计签到总天数
    continue_sign = selector.xpath('//tbody/tr[4]/td/p[2]/b/text()').get()  # 连续签到天数
    month_sign = selector.xpath('//tbody/tr[4]/td/p[3]/b/text()').get()  # 本月签到天数
    last_sign = selector.xpath('//tbody/tr[4]/td/p[4]/font/text()').get()  # 上次签到时间
    agg_score = selector.xpath('//tbody/tr[4]/td/p[5]/span[1]/b/text()').get()  # 签到总积分
    last_score = selector.xpath('//tbody/tr[4]/td/p[5]/span[2]/b/text()').get()  # 上次获得的奖励积分
    sign_lv = selector.xpath('//tbody/tr[4]/td/p[6]/span/b/text()').get()  # 目前签到等级
    replies = selector.xpath('//tbody/tr[6]/td/text()').get()  # 回帖数
    active_value = selector.xpath('//tbody/tr[7]/td/text()').get()  # 活跃值
    medal_list = selector.xpath('//tbody/tr[5]/td/ul/li/p/text()').getall()  # 勋章名称列表
    return [{
        'uid': uid, 'user_name': user_name, 'user_lv': user_lv, 'province': province,
        'active_value': active_value, 'post_num': post_num, 'replies': replies, 'friends': friends,
        'total_sign': total_sign, 'continue_sign': continue_sign, 'month_sign': month_sign,
        'last_sign': last_sign, 'agg_score': agg_score, 'last_score': last_score,
        'sign_lv': sign_lv, 'medal_num': len(medal_list)
    }]


# 功能整合 -- 获取用户详细信息 -- 单次获取 --
def get_user_info(space_url, headers):
    text = scrape_space(space_url, headers=headers)
    data = parse_space_info(text)
    dft = DataFrame(data)
    dft['dt'] = strftime('%Y-%m-%d', localtime(time()))
    print(data)
    return dft


# 功能整合 -- 获取用户详细信息 -- 全部页获取与存储
def get_user_infos(space_url_deque, headers, output_filename, encoding='utf-8'):
    for i in arange(len(space_url_deque)):
        space_url = space_url_deque.pop()
        sleep(0.01 * rand())
        print(f'第{i}条记录: ')
        print('url: ', space_url)
        dft = get_user_info(space_url, headers)
        print('=' * 100)
        append_csv(dft, filename=output_filename, encoding=encoding)


# 构造-- 精华帖子 digest -- 热门帖子 -- heat -- url
def get_digest_url(max_page: int, page_type: str):
    # digest or heat
    for page_num in arange(max_page, 0, -1):
        yield f'https://club.hihonor.com/cn/forum-3965-{page_num}.html?filter={page_type}'


# 功能整合 -- 采集精华帖 + 热门帖子 -- 用户空间 --
def get_hot_urls(max_page, page_type, headers, filename):
    generator = get_digest_url(max_page=max_page, page_type=page_type)
    while True:
        try:
            model_url = next(generator)
            text = scrape_model_page(model_url, headers)
            dft = parse_model_page(text)
            append_csv(dft, filename)
            sleep(0.1 + rand() * 0.45)
        except StopIteration:
            print('采集完成')
            break  # 终止循环, 避免死循环
