from pc_honor import get_user_infos, read_url
from clean_data import transform_excel


if __name__ == '__main__':
    headers = {
        'User-Agent': '''Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
        (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.62'''
    }

    # step1: 板块采集 page_type -- 采集用户空间url -- get_space_urls
    # '3965' -- 荣耀magic -- D1 -- 已经采集完成
    # '3159' -- 荣耀V系列 -- D2
    # '3484' -- 荣耀数字系列
    # '4280' -- 荣耀X系列 -- D4 -- 已经采集完成
    # '3666' -- 荣耀Play系列
    # '4526' -- 荣耀畅玩系列
    # model_types = [('3965', 2000), ('3159', 2000), ('3484', 2000), ('4280', 2000), ('3666', 2000), ('4526', 2000)]
    # for index, each in enumerate(model_types):
    #     page_type, max_page = each
    #     filename = './data/D' + str(index) + '.csv'
    #     sleep(180)

    # # step2 -- 采集 -- 精华帖、热门帖 -- 的用户url
    # hot_types = [
    #     (106, 'digest'), (2000, 'heat')
    # ]
    # for each in hot_types:
    #     max_page, page_type = each
    #     filename = './data/D' + page_type + '.csv'
    #     get_hot_urls(max_page, page_type, headers, filename)
    #     sleep(120)

    # # step3 -- 清洗采集到的url
    # -- 获得基础的space_urls_base -- 采集用的列表 -- space_urls
    # clean_space_urls()

    space_url_deque = read_url('./data/space_urls_active.csv', header=0)
    # 对已经存在的user_info.csv内的uid，进行清洗, 生成新的space_urls
    # if 'user_info.csv' in listdir('./data'):
    #     space_url_deque = clear_uid('user_info.csv')

    # 采集空间信息 -- 为保证字符转换不报错 -- 建议用utf-8
    get_user_infos(space_url_deque, headers=headers, output_filename='./data/user_info.csv', encoding='utf-8')
    columns = [
        'uid', 'user_name', 'user_lv', 'province', 'active_value', 'post_num', 'replies',
        'friends', 'total_sign', 'continue_sign', 'month_sign', 'last_sign', 'agg_score',
        'last_score', 'sign_lv', 'medal_num', 'date'
    ]
    # 此处注意, 手动修改 user_info1.xlsx, 已经运行过就会存在xlsx文件, 数字加1即可
    transform_excel('user_info.csv', 'user_info.xlsx', col_names=columns)
