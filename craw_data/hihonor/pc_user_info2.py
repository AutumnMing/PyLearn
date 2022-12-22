from multiprocessing import Pool
from time import strftime, localtime, time
from os import chdir, remove, getcwd
from os.path import exists
from pathlib import PurePath
from pc_honor import scrape_space, parse_space_info
from csv import DictWriter, writer
from pandas import read_csv, concat
from numpy import arange
from tqdm import tqdm


def save_user_data(user_data: dict, filename: str, mode: str):
    # 带签名的utf-8-sig可以防止乱码
    with open(filename, mode, newline='', encoding='utf-8') as f:
        w = DictWriter(f, fieldnames=list(user_data))
        w.writerow(user_data)


def creat_file(filename, filepath, columns):
    """
    创建目标csv文件, 写入表头
    :param filename:
    :param filepath:
    :param columns:
    :return:返回最后一次迭代的文件数字编号
    """
    chdir(filepath)
    if not exists(filename):
        # newline默认是换行符，如果不设置，每行之间就会有空行
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            w = writer(f)
            w.writerow(columns)  # 写入表头信息
    pure_path = PurePath(getcwd())
    print('文件创建完成,当前路径为: ', pure_path)


def check_file(filename, filepath, remove_file=False):
    """
    检查指定路径下的文件是否存在
    :param filename:
    :param filepath:
    :param remove_file:
    :return:
    """
    chdir(filepath)
    pure_path = PurePath(getcwd())
    if exists(filename) and remove_file:
        print(f'{filename}文件已存在, 删除')
        remove(filename)
    chdir(pure_path.parent)


def split_file(filename, chunksize, filepath, prefix='url_'):
    chdir(filepath)  # 切换到文件存储路径
    pure_path = PurePath(getcwd())  # 完整纯路径
    file_reader = read_csv(filename, chunksize=chunksize)
    last_file_num = 0  # 记录最后一个文件的文件编号
    for i, chunk in enumerate(file_reader, start=1):
        print(i, ' : ', len(chunk))
        chunk.to_csv(prefix + str(i) + '.csv', index=False)
        last_file_num = i
    chdir(pure_path.parent)
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
        save_user_data(user_info, desc + '_info.csv', mode='a+')
    remove(dft_name)
    print(f'{dft_name}采集完成, 已经移除文件{dft_name}')


def clean_user_info(file_list, filepath, filename, columns):
    chdir(filepath)
    dft = []
    for each_file in file_list:
        data = read_csv(each_file, encoding='utf-8', header=None)
        dft.append(data)
        remove(each_file)
    dft = concat(dft, ignore_index=True, axis=0).drop_duplicates().dropna()
    dft.columns = columns
    dft['date'] = strftime('%Y-%m-%d', localtime(time()))
    dft.to_excel(filename, index=False)
    print('采集总样本量:', len(dft))


def craw_user_info(file_path, file_name, process=4):

    # 优先检查 -- 最终输出文件是否存在 + 切换路径到数据文件夹
    check_file(file_name, filepath=file_path, remove_file=True)

    # 切割大文件, 可以根据 chunksize选择切割大小
    last_num = split_file('space_urls_active.csv', chunksize=2000, filepath=file_path, prefix='url_')
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
    clean_user_info(file_lists, file_path, file_name, col_names)


if __name__ == '__main__':
    f_path, f_name = './data', 'user_info.xlsx'
    craw_user_info(f_path, f_name, process=6)






