from os import listdir
from collections import deque
from pandas import read_csv, concat, DataFrame


def clean_space_urls():
    file_list = [each for each in listdir('./data') if each.startswith('D')]
    data = []
    for each in file_list:
        dft = read_csv('./data/' + each, header=None, encoding='utf-8')
        data.append(dft)
    # 合并
    dft = concat(data, ignore_index=True).drop_duplicates()
    dft = DataFrame(dft.values, columns=['uid', 'user_name', 'space_url'])
    # 导出
    dft.to_csv('./data/space_urls_base.csv', encoding='utf-8', index=False)
    dft.loc[:, ['space_url']].to_csv('./data/space_urls.csv', encoding='utf-8', index=False)


def clear_uid(crawed_uid, base_file='space_urls_base.txt', encoding='utf-8', index_name='uid'):

    """
    对已经采集的url信息进行清洗，从space_urls_base中移除
    :param crawed_uid:已经采集的uid所在的文件名称, txt文件, csv文件也改成txt
    :param base_file:基础的空间urls信息, 包含了uid, user_name, urls
    :param encoding:编码，推荐默认utf-8，防止中文字符报错
    :param index_name:索引列名称
    :return:包含用户空间url的csv文件
    """
    base_file = './data/' + base_file
    crawed_uid = './data/' + crawed_uid
    # header = 0表示取第一行作为字段名称, base_file表内有列名称, 报错请注意检查
    dft_base = read_csv(base_file, header=0, encoding=encoding, dtype={index_name: 'str'})
    print(dft_base)
    # 注意查看 use_info_crawed 有没有表头、默认第一列是 uid -- 这里的写法是认为有
    uid_crawed = read_csv(crawed_uid, header=0, encoding=encoding, dtype={index_name: 'str'})
    uid_crawed_list, all_uid_list = uid_crawed.loc[:, index_name].tolist(), dft_base.loc[:, index_name].tolist()
    print('已采集的url数目: ', len(uid_crawed_list))
    print('需采集的url总数: ', len(all_uid_list))
    other_uid_list = [uid for uid in all_uid_list if uid not in uid_crawed_list]
    url_list = dft_base.set_index(index_name).loc[other_uid_list, 'space_url'].tolist()
    print('未采集的url数目: ', len(url_list))
    return deque(url_list)


def transform_excel(csv_name, excel_name, col_names, encoding='utf-8', uid_col=('uid',0)):
    if 'data' not in csv_name:
        csv_name = './data/' + csv_name
        if 'data' not in excel_name:
            excel_name = './data/' + excel_name
    uid_name, uid_index = uid_col # 解包元组获取uid的名称, 所在列
    # dtype参数定义uid为字符串
    dft = read_csv(csv_name, encoding=encoding, header=None, dtype={uid_index:str}).dropna().drop_duplicates()
    dft = DataFrame(data=dft.values, columns=col_names)
    # 顺带对csv文件进行去重 -- 去除空行 -- 添加表头
    dft.to_csv(csv_name, encoding=encoding, index=False, header=True)
    dft.to_excel(excel_name, index=False)
    print('csv已经转换成xlsx')


# 测试代码,输出的测试文件可以删除
if __name__ == '__main__':

    # columns = [
    #     'uid', 'user_name', 'user_lv', 'province', 'active_value', 'post_num', 'replies',
    #     'friends', 'total_sign', 'continue_sign', 'month_sign', 'last_sign', 'agg_score',
    #     'last_score', 'sign_lv', 'medal_num', 'date'
    # ]
    # transform_excel('user_info.csv', 'user_info.xlsx', col_names=columns)

    # 测试 transform_excel
    columns=['uid','name']
    transform_excel('test.csv', 'test.xlsx', col_names=columns)


