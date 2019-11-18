from time import sleep


def test_radio(driver):
    driver.get("http://ui.yansl.com/#/radio")

    #点击性别女
    driver.click("xpath=>//label[text()='纯单选框']/../div/input[1]")
    #点击备选框2
    driver.click("xpath=>//label[text()='单选框2']/../div/label[1]//input")
    #点击上海
    driver.click("xpath=>//label[text()='单选框3']/../div//span[text()='上海']")
    #assert '上海' in driver.driver.page_source