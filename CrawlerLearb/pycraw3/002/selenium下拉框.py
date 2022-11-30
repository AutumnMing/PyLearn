# 中国行政区划,用于学习selenium下拉框
# 不做爬取速度、函数优化
# 网站本身加载速度较慢,请通过sleep增加等待时间,不要给网站服务器增加压力
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

browser = webdriver.Edge()
browser.get('http://xzqh.mca.gov.cn/map')

# 获取全部的省份列表下拉框
select_prov_element = browser.find_element(By.NAME, 'shengji')
select_prov = Select(select_prov_element)

# 获取指定省份的所有地级市
select_city_element = browser.find_element(By.NAME, 'diji')
select_city = Select(select_city_element)

# 获取指定地级市的区县
select_district_element = browser.find_element(By.NAME, 'xianji')
select_district = Select(select_district_element)

# 获取全部省份列表
shengji_list = select_prov.options
prov_list = [each.text for each in shengji_list[1:]]

# 从省份循环采集
for prov in prov_list:
    print('='*100)
    select_prov.select_by_value(prov)
    sleep(1.5)
    diji_list = select_city.options

    # 获得每个省份的地级市列表
    city_list = [each.text for each in diji_list[1:]]

    # 获取每个省份每个地级市的区县列表
    for city in city_list:
        select_city.select_by_value(city)
        sleep(1.5)
        xianji_list = select_district.options
        print('正在获取数据: ', prov, '--', city)
        district_list = [
            {'prov': prov, 'city': city, 'district': each.text}
            for each in xianji_list[1:]
        ]

    print('='*100)
    sleep(0.5)


browser.close()
print('关闭浏览器')
