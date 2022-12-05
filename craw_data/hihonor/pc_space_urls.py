from pc_honor import get_space_urls
from pc_honor import get_hot_urls
from clean_data import clean_space_urls
from time import sleep

# step1: 板块采集 page_type -- 采集用户空间url -- get_space_urls
# '3965' -- 荣耀magic -- D1 -- 已经采集完成
# '3159' -- 荣耀V系列 -- D2
# '3484' -- 荣耀数字系列
# '4280' -- 荣耀X系列 -- D4 -- 已经采集完成
# '3666' -- 荣耀Play系列
# '4526' -- 荣耀畅玩系列
if __name__ == '__main__':
    headers = {
        'User-Agent': '''Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
        (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.62'''
    }

    model_types = [('3965', 2000), ('3159', 2000), ('3484', 2000), ('4280', 2000), ('3666', 2000), ('4526', 2000)]
    for index, each in enumerate(model_types):
        page_type, max_page = each
        filename = './data/D' + str(index) + '.csv'
        get_space_urls(max_page, page_type, headers, filename)
        sleep(180)

    # step2 -- 采集 -- 精华帖、热门帖 -- 的用户url
    hot_types = [(106, 'digest'), (2000, 'heat')]
    for each in hot_types:
        max_page, page_type = each
        filename = './data/D' + page_type + '.csv'
        get_hot_urls(max_page, page_type, headers, filename)
        sleep(120)

    # step3 -- 清洗采集到的url
    # -- 获得基础的space_urls_base -- 采集用的列表 -- space_urls
    clean_space_urls()
