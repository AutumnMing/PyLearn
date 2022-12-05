import os


os.getcwd()
# 测试文件
a: list[int] = [1, 2, 3, 4, 5]


b: list[int] = [1, 2, 3]


dict_a: dict[str:int] = {'a':1, 'b':2, 'c':3}
print('原始字典a', dict_a, sep=' : ')
dict_b: dict[str:int] = {'a':100}
_ = dict_a | dict_b
print('更新后的字典a', dict_a, sep=' : ')

