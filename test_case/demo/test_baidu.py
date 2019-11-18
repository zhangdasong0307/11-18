# -*- coding:utf-8 -*-
# Author : 小吴老师
# Data ：2019/7/31 15:15
from time import sleep


def test_baidu(driver):
    driver.get('http://www.baidu.com')
    driver.send_keys("id=>kw",'手机')
    sleep(3)
    assert '百度' in driver.driver.page_source


def test_radio(driver):
    driver.get("http://ui.yansl.com/#/radio")

    #点击性别女
    driver.click("xpath=>//*[@id='form']/form/div[1]/div/input[2]")
    #点击备选框2
    driver.click("xpath=>//*[@id='form']/form/div[2]/div/div/label[3]/span[1]/span")
    #点击上海
    driver.click("xpath=>//*[@id='form']/form/div[3]/div/div/label[2]/span")
    assert '上海' in driver.driver.page_source


def test_input(driver):
    driver.get("http://ui.yansl.com/#/input")
    driver.send_keys("xpath=>//*[@id='form']/form/div[1]/div/input","遮天")
    driver.send_keys('xpath=>//*[@id="form"]/form/div[2]/div/input',"zhetian")
    driver.send_keys('xpath=>//*[@id="form"]/form/div[3]/div/textarea',"完美世界")

def test_checkbox(driver):
    driver.get("http://ui.yansl.com/#/checkbox")
    #点击上海
    driver.click('xpath=>//*[@id="form"]/form/div[1]/div/input[1]')
    #点击mysql
    driver.click('xpath=>//*[@id="form"]/form/div[2]/div/div/label[2]/span[1]/span')
    #点击上海，北京
    driver.click('xpath=>//*[@id="form"]/form/div[3]/div/div[2]/label[1]/span[1]/span')
    driver.click('xpath=>//*[@id="form"]/form/div[3]/div/div[2]/label[2]/span[1]/span')
    #点击广州，深圳
    driver.click('xpath=>//*[@id="form"]/form/div[4]/div/div/label[3]/span')
    driver.click('xpath=>//*[@id="form"]/form/div[4]/div/div/label[4]/span')


