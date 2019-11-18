import allure
import json
from tools.report import log_tool
from tools.data import string_tool
from tools.report import assert_tool
# 项目根目录建config包，里面建conf.py文件，用于配置
from config import conf
from tools.data.json_path_tool import *

# log decorator
def logs(func):
    def _func(*args, **kwargs):
        r= func(*args, **kwargs)
        request = "-------------------request-------------" \
                  "\n{0}\n{1}\n{2}".format(r.url, string_tool.dic_to_str(r.request.headers), r.request.body)
        log_tool.info(request)
        response = "---------------response----------------" \
                   "\n{0}\n{1}\n{2}".format(r.status_code, string_tool.dic_to_str(r.headers), r.text)
        log_tool.info(response)
        allure.attach(request,'request',allure.attachment_type.TEXT)
        allure.attach(response, 'response', allure.attachment_type.TEXT)
        return r
    return _func



# screenshot decorator
def shot(func):
    def function(*args, **kwargs):
        allure.attach(args[0].driver.get_screenshot_as_png(), args[1] + '之前', allure.attachment_type.PNG)
        i = 1
        res = None
        while(i <= 3):
            try:
                res = func(*args, **kwargs)
                break
            except :
                if i == 3:
                    allure.attach(args[0].driver.get_screenshot_as_png(), args[1] + '之后', allure.attachment_type.PNG)
                    raise
                i += 1
        allure.attach(args[0].driver.get_screenshot_as_png(), args[1] + '之后', allure.attachment_type.PNG)
        return res
    return function


def is_empty(a):
    if isinstance(a,int) or not a:
        return True
    elif(isinstance(a,str) and len(a)==0):
        return True
    return False



def datas(func):
    def function(*args,**kwargs):
        data=kwargs.pop("pub_data")
        d = kwargs
        keys = list(kwargs.keys())
        for k in ['json_data','json']:
            if k in keys :
                keys.remove(k)
                value = d.pop(k)
                if (isinstance(value, str)):
                    d['json'] = json.loads(value)
                else:
                    d['json']=value
        with allure.step("第一步：获取url"):
            pass
        if 'uri' in keys:
            keys.remove('uri')
            value = d.pop('uri')
            d['url'] = value
        for k in ["feature",'story','tag','testcase','description','title','issue','link','mro','severity']:
            if k in keys:
                keys.remove(k)
                value = d.pop(k)
                if not is_empty(value)  and isinstance(value,list):
                    getattr(allure.dynamic, k)(*value)
                elif(not is_empty(value)  and isinstance(value,str)):
                    getattr(allure.dynamic, k)(value)
        with allure.step("第二步：准备测试数据"):pass
        try:
            index_dic(data, data)
            index_dic(d,data)
        except:
            pass
        if "url" not in keys:
            print("请输入正确的uri")
        if 'http://' not in d["url"]:
            d["url"] = conf.API_URL + d["url"]
        for s in ["status_code",'expect',"json_path"]:
            if s in keys:
                keys.remove(s)
                exec("{} = d.pop(s)".format(s))

            else:
                exec("{}=None".format(s))
        with allure.step("第三步：发送请求"):
            resp = func(*args,**kwargs)
        try:
            exec('''
if(len(json_path) != 0):
    for path in json_path:
        get_json_data(resp.json(),path,data)''')

        except:
            pass
        a = '''
if not is_empty(status_code):    
    # 判断响应码
    allure.attach("预期结果：{}\\n------------------------------------------------------\\n实际结果：{}".format(status_code, resp.status_code), "响应状态码断言", allure.attachment_type.TEXT)
    assert_tool.assert_equal(resp.status_code, status_code)
if not is_empty(expect):
    # 判断响应码
    allure.attach("预期结果：{}\\n------------------------------------------------------\\n实际结果：{}".format(expect, resp.text), "响应正文断言", allure.attachment_type.TEXT)
    assert_tool.assert_in(resp.text, expect)'''
        with allure.step("第四步：判断结果"):
            exec(a)

        return resp
    return function





