from multiprocessing import Pool
from time import strftime, localtime, time
from functools import wraps
from os import chdir, remove, getcwd
from os.path import exists
from pathlib import PurePath
from pc_honor import scrape_space, parse_space_info
from csv import DictWriter
from pandas import read_csv, concat
from numpy import arange
from tqdm import tqdm


def check_path(function_name):
    """
    一个自动检查文件路径的装饰器, 注意被装饰的函数第一个参数必须为路径
    :param function_name:
    :return:
    """
    # 判断当前路径是否和同一根目录下的目标路径一致
    @wraps(function_name)
    def wrapper(*args, **kwargs):
        print('=' * 150)
        print(f'即将执行函数: {function_name.__name__}')
        # 对传入的位置参数解包, 注意所有的被装饰函数, filepath必须是第一个
        filepath, *_ = args
        cwd_path, filepath = PurePath(getcwd()), PurePath(filepath)
        print(f'当前路径为: {cwd_path}')
        # 完整路径相等 或者 相对路径, 最后一个文件一样
        if not (cwd_path == filepath or cwd_path.parts[-1] == filepath):
            chdir(filepath)
            print(f'已经切换至目标路径: {PurePath(getcwd())}')
        # print(args)
        fun = function_name(*args, **kwargs)
        return fun
    return wrapper


def save_user_data(filename: str, user_data: dict, mode: str):
    # 带签名的utf-8-sig可以防止乱码
    with open(filename, mode, newline='', encoding='utf-8') as f:
        w = DictWriter(f, fieldnames=list(user_data))
        w.writerow(user_data)


# @check_path
# def creat_file(filepath, filename, columns):
#     """
#     创建目标csv文件, 写入表头
#     :param filepath:
#     :param filename:
#     :param columns:
#     :return:返回最后一次迭代的文件数字编号
#     """
#     print(f'目标路径为: {filepath}')
#     if not exists(filename):
#         # newline默认是换行符，如果不设置，每行之间就会有空行
#         with open(filename, 'w', newline='', encoding='utf-8') as f:
#             w = writer(f)
#             w.writerow(columns)  # 写入表头信息
#

@check_path
def check_file(filepath, filename, remove_file=False):
    """
    检查指定路径下的文件是否存在
    :param filepath:
    :param filename:
    :param remove_file:
    :return:
    """
    if exists(filename) and remove_file:
        print(f'{filename}文件已存在, 删除')
        remove(filename)
    print(f'函数执行完成, 存储路径为: {filepath}')
    print('=' * 150)


@check_path
def split_file(filepath, filename, chunksize, prefix='url_'):
    print(f'文件名称: {filename}, 单个文件满记录数: {chunksize}')
    file_reader = read_csv(filename, chunksize=chunksize)
    last_file_num = 0  # 记录最后一个文件的文件编号
    for i, chunk in enumerate(file_reader, start=1):
        # print(i, ' : ', len(chunk))
        chunk.to_csv(prefix + str(i) + '.csv', index=False)
        last_file_num = i
    print(f'函数执行完成, 存储路径为: {filepath}')
    print('=' * 150)
    return last_file_num


def get_user_info(dft_name):
    """
    传入目标url文件名称,采集目标url的用户信息
    :param dft_name:
    :return:
    """
    dft = read_csv(dft_name)
    headers = {
        'User-Agent': '''Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
        (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.62'''
    }
    desc = dft_name.partition('.csv')[0]  # 获取进度条显示字符
    for href in tqdm(dft.loc[:, 'space_url'].tolist(), desc=desc):
        res_text = scrape_space(href, headers)
        user_info = parse_space_info(res_text)
        # 插入不同的数据文件, 免得数据混淆
        save_user_data(desc + '_info.csv', user_info, mode='a+')
    remove(dft_name)
    print(f'{dft_name}采集完成, 已经移除文件{dft_name}')


def clean_user_info(filename, columns, file_list):
    dft = []
    for each_file in file_list:
        data = read_csv(each_file, encoding='utf-8', header=None)
        dft.append(data)
        remove(each_file)
    dft = concat(dft, ignore_index=True, axis=0).drop_duplicates().dropna()
    dft.columns = columns
    dft['date'] = strftime('%Y-%m-%d', localtime(time()))
    dft.to_excel(filename, index=False)
    print(f'清洗后文件名: {filename}, 采集总样本量:', len(dft))


def craw_user_info(file_path, file_name, process=4):

    # 切割大文件, 可以根据 chunksize选择切割大小
    last_num = split_file(file_path, filename='space_urls_active.csv', chunksize=2000, prefix='url_')
    # 生成文件读取列表
    file_name_list = ['url_' + str(i) + '.csv' for i in arange(1, last_num + 1)]
    # 开启进程池, 采集数据 --  get_user_info(dft_name)
    with Pool(processes=process) as pool:
        pool.map(get_user_info, file_name_list)
        pool.close()
        pool.join()

    # 最终文件合并 + 数据清洗
    col_names = [
        'uid', 'user_name', 'user_lv', 'province', 'active_value', 'post_num', 'replies',
        'friends', 'total_sign', 'continue_sign', 'month_sign', 'last_sign', 'agg_score',
        'last_score', 'sign_lv', 'medal_num'
    ]
    file_lists = ['url_' + str(i) + '_info.csv' for i in arange(1, last_num + 1)]
    clean_user_info(file_name, col_names, file_lists)


if __name__ == '__main__':
    f_path, f_name = './data', 'user_info.xlsx'
    craw_user_info(f_path, f_name, process=12)
