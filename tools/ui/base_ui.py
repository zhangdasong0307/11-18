# coding=utf-8
import allure
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.select import Select
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

from config.config import ROOT_PATH
from tools.report import log_tool
from tools.os import os_tool




class BaseUI:

    original_window = None

    def __init__(self, browser='chrome',timeout=10):
        '''
        :param browser: 浏览器类型
        :param timeout: 显示等待超时时间
        '''
        self.driver = None
        if browser == "firefox" or browser == "ff":
            self.driver = webdriver.Firefox()
        elif browser == "chrome":
            driver_path = ROOT_PATH
            self.driver = webdriver.Chrome(driver_path)
            self.driver.maximize_window()
            self.driver.implicitly_wait(10)
        elif browser == "internet explorer" or browser == "ie":
            self.driver = webdriver.Ie()
        elif browser == "opera":
            self.driver = webdriver.Opera()
        elif browser == "chrome_headless":
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            self.driver = webdriver.Chrome(ROOT_PATH,chrome_options=chrome_options)
        elif browser == 'edge':
            self.driver = webdriver.Edge()
        else:
            log_tool.error("启动浏览器失败，没有找到%s浏览器，请输入'ie', 'ff', 'opera', 'edge', 'chrome' or 'chrome_headless'"% browser)
            raise NameError(
                "启动浏览器失败，没有找到%s浏览器，请输入'ie', 'ff', 'opera', 'edge', 'chrome' or 'chrome_headless'"% browser)
        self.timeout = timeout
        self.location_type_dict = {
            "xpath": By.XPATH,
            "id": By.ID,
            "name": By.NAME,
            "css_selector": By.CSS_SELECTOR,
            "class_name": By.CLASS_NAME,
            "tag_name": By.TAG_NAME,
            "link_text": By.LINK_TEXT,
            "partial_link_text": By.PARTIAL_LINK_TEXT
        }

    def shot(self,*args, **kwargs):
        log_tool.info(" ".join(args))
        allure.attach(self.driver.get_screenshot_as_png()," ".join(args),allure.attachment_type.PNG)

    def max_window(self):
        '''
        最大化浏览器
        :return:
        '''
        self.shot("最大化浏览器")
        self.driver.maximize_window()

    def set_window(self, wide, high):
        '''
        设置浏览器大小
        :param wide: 宽
        :param high: 高
        :return:
        '''
        self.shot("设置浏览器大小,宽：",wide,"高",high)
        self.driver.set_window_size(wide, high)

    def close(self):
        '''
        关闭浏览器，不退出driver
        :return:
        '''
        self.shot("关闭浏览器，不退出driver")
        self.driver.close()

    def quit(self):
        '''
        关闭浏览器并退出driver
        :return:
        '''
        self.shot("关闭浏览器并退出driver")
        self.driver.quit()


    def get(self, url):
        '''
        打开网址
        :param url:网址
        :return:
        '''
        self.shot("打开网址：",url)
        self.driver.get(url)


    def forward(self):
        '''
        前进
        :return:
        '''
        self.driver.forward()
        self.shot("前进")


    def back(self):
        '''
        后退
        :return:
        '''
        self.driver.back()
        self.shot("后退")


    def refresh(self):
        '''
        刷新
        :return:
        '''

        self.driver.refresh()
        self.shot("刷新")

    def get_title(self):
        '''
        获取当前页面的title
        :return: title
        '''
        self.shot("获取当前页面的title:",self.driver.title)
        return self.driver.title

    def get_url(self):
        '''
        获取当前页面的网址
        :return: url
        '''
        self.shot("获取当前页面的url",self.driver.current_url)
        return self.driver.current_url

    def get_locator(self, locator):
        '''
        解析定位关键字
        :param locator:定位语句 例如：xpath=>//*[@id='kw']
        :return: 元组(By.XPATH,"//*[@id='kw']")
        '''
        if "=>" not in locator and "xpath" not in locator:
            by = "xpath"
            value = locator
        elif("=>" in locator):
            by = locator.split("=>")[0].strip()
            value = locator.split("=>")[1].strip()
            if by not in (self.location_type_dict):
                log_tool.error("%s中的定位方式错误，请输入正确的定位方式:"
                                "id,name,class_name,xpath,tag_name,css_selector,link_text,partial_link_text"%(locator))
                raise TypeError("%s中的定位方式错误，请输入正确的定位方式:"
                                "id,name,class_name,xpath,tag_name,css_selector,link_text,partial_link_text"%(locator))
            if by == "" or value == "":
                log_tool.error("%s格式错误，定位方式=>值 示例：'id=>useranme'"%(locator))
                raise NameError("%s格式错误，定位方式=>值 示例：'id=>useranme'"%(locator))
        else:
            log_tool.error("%s格式错误，定位方式=>值 示例：'id=>useranme'" % (locator))
            raise NameError("%s格式错误，定位方式=>值 示例：'id=>useranme'"%(locator))
        return (self.location_type_dict[by],value)

    def get_page_source(self):
        '''
        返回页面源代码
        :return: 页面源代码
        '''
        self.shot("获取页面源代码")
        return self.driver.page_source


    def get_element(self,locator):
        '''
        根据传入的数据来定位页面元素
        :param locator: 定位语句 例如：xpath=>//*[@id='kw']
        :return: 元素定位结果
        '''
        self.shot("定位元素",locator)
        local = self.get_locator(locator)
        time_out_error = "{}定位元素超时，请检查定为语句是否正确，或者尝试其他定位方式".format(local)
        try:
            return WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located(local))
        except TimeoutException:
            log_tool.error(time_out_error)
            raise TimeoutException(time_out_error)


    def send_keys(self, locator, text):
        '''
        先清空文本输入框，再输入内容
        :param locator: 定位语句 例如：xpath=>//*[@id='kw']
        :param text: 输入的文本内容
        :return:
        '''
        element = self.get_element(locator)
        ActionChains(self.driver).click(element).key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).send_keys(
            Keys.BACKSPACE).perform()

        element.send_keys(text)
        self.shot( "输入：", text)




    def click(self, locator):
        '''
        左键单击操作
        :param locator: 定位语句 例如：xpath=>//*[@id='kw']
        :return:
        '''
        element = self.get_element(locator)
        ActionChains(self.driver).move_to_element(element).click().perform()
        self.shot("点击")


    def right_click(self, locator):
        '''
        右键单击操作
        :param locator: 定位语句 例如：xpath=>//*[@id='kw']
        :return:
        '''
        el = self.get_element(locator)
        ActionChains(self.driver).context_click(el).perform()
        self.shot("右击")


    def double_click(self, locator):
        '''
        左键双击操作
        :param locator: 定位语句 例如：xpath=>//*[@id='kw']
        :return:
        '''
        el = self.get_element(locator)
        ActionChains(self.driver).double_click(el).perform()
        self.shot("双击")


    def move_to_element(self, locator):
        '''
        鼠标移动到元素上方，并保持悬浮
        :param locator: 定位语句 例如：xpath=>//*[@id='kw']
        :return:
        '''
        el = self.get_element(locator)
        ActionChains(self.driver).move_to_element(el).perform()
        self.shot("鼠标移动到元素上方，并保持悬浮")


    def drag_and_drop(self, el_locator, ta_locator):
        '''
        拖拽一个元素到另一个元素
        :param el_locator: 要拖拽的元素，定位语句 例如：xpath=>//*[@id='kw']
        :param ta_locator: 拖拽的目标元素，定位语句 例如：xpath=>//*[@id='kw']
        :return:
        '''
        element = self.get_element(el_locator)
        target = self.get_element(ta_locator)
        ActionChains(self.driver).drag_and_drop(element, target).perform()
        self.shot("把第一个元素拖拽到第二个元素的位置")



    def submit(self, locator):
        '''
        对元素执行表单提交操作
        :param locator: 定位语句 例如：xpath=>//*[@id='kw']
        :return:
        '''
        el = self.get_element(locator)
        el.submit()
        self.shot("执行表单操作")



    def execute_script(self, script):
        '''
        执行js代码
        :param script:
        :return:
        '''
        self.driver.execute_script(script)
        self.shot("执行js脚本:", script)

    def get_attribute(self, locator, attribute):
        '''
        获取元素属性的值
        :param locator:定位语句 例如：xpath=>//*[@id='kw']
        :param attribute: 属性名
        :return: 属性值
        '''
        el = self.get_element(locator)
        value = el.get_attribute(attribute)
        self.shot("获取元素属性：{} 的值为：{}".format(attribute,value))
        return value

    def get_text(self, locator):
        '''
        获取元素展示文本
        :param locator:定位语句 例如：xpath=>//*[@id='kw']
        :return: 展示文本
        '''
        el = self.get_element(locator)
        text = el.text
        self.shot("获取元素的展示文本为：", text)
        return text

    def is_display(self, locator):
        '''
        判断元素是否可见
        :param locator: 定位语句 例如：xpath=>//*[@id='kw']
        :return: 可见为true 不可见为false
        '''
        el = self.get_element(locator)
        display = el.is_displayed()
        return display


    def get_alert_text(self):
        '''
        获取弹框的展示文本
        :return:展示文本
        '''
        text = self.driver.switch_to.alert.text
        self.shot("弹框的展示文本为：", text)
        return text


    def alert_accept(self):
        '''
        切换到弹框并确认
        :return:
        '''
        self.driver.switch_to.alert.accept()
        self.shot("窗口切换至弹框并接受")


    def alert_dismiss(self):
        '''
        切换至弹框，并取消
        :return:
        '''
        self.driver.switch_to.alert.dismiss()
        self.shot("窗口切换至弹框并取消")


    def switch_to_frame(self, locator):
        '''
        切入iframe框架里边
        :param locator: 定位语句 例如：xpath=>//*[@id='kw']
        :return:
        '''
        iframe_el = self.get_element(locator)
        self.driver.switch_to.frame(iframe_el)
        self.shot("切入iframe")


    def switch_to_frame_out(self):
        '''
        切出iframe
        :return:
        '''
        self.driver.switch_to.default_content()
        self.shot("退出iframe，回到初始页面")


    def switch_to_windows_by_title(self, title):
        '''
        #切换到名字为title的窗口
        :param title: 窗口标题
        :return: 返回值：当前窗口的句柄
        '''
        current = self.driver.current_window_handle
        handles = self.driver.window_handles
        for handle in handles:
            self.driver.switch_to.window(handle)
            if (self.driver.title.__contains__(title)):
                break
        return current

    def screenshot(self, file_path):
        '''
        截图
        :param file_path: 文件路径
        :return:
        '''
        self.driver.get_screenshot_as_file(file_path)


    def select_by_value(self, locator, value):
        '''
        操作select标签，根据标签的value属性值选择
        :param locator: 定位语句 例如：xpath=>//*[@id='kw']
        :param value: select标签value属性的值
        :return:
        '''
        el = self.get_element(locator)
        Select(el).select_by_value(value)
        self.shot("选择value值为：{} 的元素".format(value))


    def select_by_index(self, locator, value):
        '''
        操作select标签，根据选项的下标选择，下标从0开始
        :param locator: 定位语句 例如：xpath=>//*[@id='kw']
        :param value: 选项的下标
        :return:
        '''
        el = self.get_element(locator)
        Select(el).select_by_index(value)
        self.shot("选择第 {} 个元素".format(value))


    def select_by_text(self, locator, value):
        '''
        操作select标签，根据选项的展示文本选择
        :param locator: 定位语句 例如：xpath=>//*[@id='kw']
        :param value: 下拉选项的展示文本
        :return:
        '''
        el = self.get_element(locator)
        Select(el).select_by_visible_text(value)
        self.shot("选择{}".format(value))

    def sleep(self, sec):
        '''
        线程休眠
        :param sec: 秒数
        :return:
        '''
        time.sleep(sec)

    def wait_time(self, secs):
        '''
        元素定位的隐式等待
        :param secs: 最长秒数
        :return:
        '''
        self.driver.implicitly_wait(secs)


    def wait_util_presence(self,locator,secs=10):
        '''
        显示等待页面元素出现在DOM中，但并不一定可见，存在则返回该页面元素对象
        :param locator: 定位语句 例如：xpath=>//*[@id='kw']
        :param secs: 最长等待时间
        :return:元素对象
        '''
        locator = self.get_locator(locator)
        try:
            element = WebDriverWait(self.driver, secs).until(
                        EC.presence_of_element_located(locator))
            return element
        except Exception as e:
            raise e


    def wait_util_visibility(self, locator, secs=10):
        '''
        显示等待页面元素的出现，并返回元素对象
        :param locator: 定位语句 例如：xpath=>//*[@id='kw']
        :param secs: 最长等待时间
        :return:元素对象
        '''
        locator = self.get_locator(locator)
        try:
            element = WebDriverWait(self.driver, secs).until(
                EC.visibility_of_element_located(locator))
            return element
        except Exception as e:
            raise e

    def wait_util_not_visibility(self, locator, secs=10):
        '''
        显示等待页面元素不可见
        :param locator: 定位语句 例如：xpath=>//*[@id='kw']
        :param secs: 最长等待时间
        :return:
        '''
        locator = self.get_locator(locator)
        try:
            WebDriverWait(self.driver, secs).until(
                EC.invisibility_of_element_located(locator))

        except Exception as e:
            raise e

    def wait_util_clickable(self, locator, secs=10):
        '''
        判断某个元素中是否可见并且是可点击的，并返回元素对象
        :param locator: 定位语句 例如：xpath=>//*[@id='kw']
        :param secs: 等待超时时间
        :return:元素对象
        '''
        locator = self.get_locator(locator)
        try:
            element = WebDriverWait(self.driver, secs).until(
                EC.element_to_be_clickable(locator))
            return element
        except Exception as e:
            raise e

    def wait_util_selected(self, locator, secs=10):
        '''
        判断某个元素是否被选中了,一般用在select下拉框
        :param locator: 定位语句 例如：xpath=>//*[@id='kw']
        :param secs: 等待超时时间
        :return:
        '''
        locator = self.get_locator(locator)
        try:
            element = WebDriverWait(self.driver, secs).until(
                EC.element_to_be_selected(locator))
            return element
        except Exception as e:
            raise e

    def wait_util_text(self, locator,text, secs=10):
        '''
        判断text是否存在于元素展示文本中
        :param locator: 定位语句 例如：xpath=>//*[@id='kw']
        :param text: 判断内容
        :param secs: 等待超时时间
        :return: 存在返回：true 不存在返回：flase
        '''
        locator = self.get_locator(locator)
        try:
            is_true = WebDriverWait(self.driver, secs).until(
                EC.text_to_be_present_in_element(locator,text))
            return is_true
        except Exception as e:
            raise e

    def wait_util_at_lest_one(self,locator, secs=10):
        '''
        判断是否至少有1个元素存在于dom树中，如果定位到就返回列表
        :param locator: 定位语句 例如：xpath=>//*[@id='kw']
        :param secs: 等待超时时间
        :return: 定位到的元素对象列表
        '''
        locator = self.get_locator(locator)
        try:
            items = WebDriverWait(self.driver, secs).until(
                EC.presence_of_all_elements_located(locator))
            return items
        except Exception as e:
            raise e




    def wait_util_title_is(self,title, secs=10):
        '''
        判断页面标题和title相等
        :param title: 指定标题内容
        :param secs: 等待超时时间
        :return: 相等返回：true 不相等返回：false
        '''
        try:
            is_true = WebDriverWait(self.driver, secs).until(
                EC.title_is(title))
            return is_true
        except Exception as e:
            raise e

    def wait_util_title_contains(self, title, secs=10):
        '''
        显示等待页面title包含指定内容
        :param title: 标题指定内容
        :param secs: 等待超时时间
        :return: 包含返回：true，不包含返回：false
        '''
        try:
            is_true = WebDriverWait(self.driver, secs).until(
                EC.title_contains(title))
            return is_true
        except Exception as e:
            raise e


    def wait_util_alert_present(self, secs=10):
        '''
        判断页面上是否存在alert,如果有就切换到alert
        :param secs: 等待超时时间
        :return: 弹框对象
        '''
        try:
            return WebDriverWait(self.driver, secs).until(
                EC.alert_is_present())
        except Exception as e:
            raise e

    def wait_util_frame_available(self, locator, secs=10):
        '''
        检查frame是否存在，存在则切换进去
        :param locator:定位语句 例如：xpath=>//*[@id='kw']
        :param secs: 等待超时时间
        :return:
        '''
        locator = self.get_locator(locator)
        try:
            WebDriverWait(self.driver, secs).until(
                EC.frame_to_be_available_and_switch_to_it(locator))
        except Exception as e:
            raise e
