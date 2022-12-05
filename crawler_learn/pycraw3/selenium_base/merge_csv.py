from os import listdir, chdir, getcwd, remove
from pandas import read_csv, concat
from pandas.errors import EmptyDataError

base_path = getcwd()
print(base_path)
chdir('./data')

data = []
for each in listdir():
    print('='*100)
    try:
        df = read_csv(each)
        print('正在读取: ', each, '总共', len(df), '样本')
        data.append(df)
        remove(each)
    except EmptyDataError:
        print(EmptyDataError)
        print(each, '问题区域')

# chdir(base_path)
df = concat(data)
df.to_csv('district.csv', index=False, encoding='utf-8')
print(len(df))
