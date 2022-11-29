# 用来测试一些包安装是否成功
from selenium import webdriver
from time import sleep

browser = webdriver.Chrome()
browser.get('https://www.baidu.com')
sleep(5)
browser.close()
