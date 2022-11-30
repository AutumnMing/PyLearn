#
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

browser = webdriver.Edge()
browser.get('http://xzqh.mca.gov.cn/map')

# 获取全部的省份列表
select_prov_element = browser.find_element(By.NAME, 'shengji')
select_prov = Select(select_prov_element)
shengji_list = select_prov.options
prov_list = [each.text for each in shengji_list[1:]]

# 获取指定省份的所有地级市
select_city_element = browser.find_element(By.NAME, 'diji')
select_city = Select(select_city_element)

for prov in prov_list:
    print('='*100)
    print('正在获取', prov, '地级市')
    print('='*100)
    select_prov.select_by_value(prov)
    sleep(1.5)
    diji_list = select_city.options
    city_list = [{'prov': prov, 'city': each.text} for each in diji_list[1:]]
    sleep(0.5)
    print(city_list)

browser.close()
print('关闭浏览器')
