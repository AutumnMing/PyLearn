from multiprocessing import Process, Lock, Pool
from time import strftime, localtime, time
from pc_honor import get_user_info, read_url, append_csv
from clean_data import transform_excel


class GetUsersInfo(Process):
    def __init__(self, urls_lists, headers, output_name, encodings='utf-8'):
        Process.__init__(self)
        self.urls_lists = urls_lists
        self.headers = headers
        self.output_name = output_name
        self.encodings = encodings
        self.lock = Lock()

    def run(self):
        for space_url in self.urls_lists:
            print('=' * 100)
            print('Process_id: ', str(self.pid))
            print('Space_url: ', space_url)
            dft = get_user_info(space_url, self.headers)
            # 数据锁防止混淆输出
            self.lock.acquire()
            append_csv(dft, filename=self.output_name, encoding=self.encodings)
            self.lock.release()


if __name__ == '__main__':

    header = {
        'User-Agent': '''Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
        (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.62'''
    }
    print(header)
    # step4 -- space_urls_active 是已经清洗完成的活跃用户
    # space_urls_data = read_url('./data/space_urls_active.csv', header=0, chunksize=30)
    # out_name, encoding = './data/user_info.csv', 'utf-8'
    # # 开启4个进程
    # with Pool(4) as p:
    #     for space_urls_lists in space_urls_data:
    #         get_info_obj = GetUsersInfo(space_urls_lists, header, out_name, encoding)
    #         get_info_obj.start()
    #         get_info_obj.join()
    #         get_info_obj.close()
    #
    # # 转换文件格式, 添加表头
    # columns = [
    #     'uid', 'user_name', 'user_lv', 'province', 'active_value', 'post_num', 'replies',
    #     'friends', 'total_sign', 'continue_sign', 'month_sign', 'last_sign', 'agg_score',
    #     'last_score', 'sign_lv', 'medal_num', 'date'
    # ]
    # out_name = 'user_info' + strftime('%Y%m%d%H', localtime(time())) + '.xlsx'
    # transform_excel('user_info.csv', out_name, col_names=columns)
