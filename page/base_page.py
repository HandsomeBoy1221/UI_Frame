import json
import time

import yaml
from appium.webdriver.common.mobileby import MobileBy
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from UI_Frame.page.handle_black import handle_black

#所有的page继承于此基类，可将常用方法封装于此页面，减少driver的直接调用
class BasePage:
    _black_list = [
        (By.ID, "com.xueqiu.android:id/iv_close")
    ]
    _max_err_num = 3
    _error_num = 0
    _params = {}

    def __init__(self,driver:WebDriver=None):
        self.driver=driver

#调用自定义的装饰器，在find出现异常时进入黑名单查找元素
    @handle_black
    def find(self, by, locator=None):
        if locator is None:
            result = self.driver.find_element(*by)
        else:
            result = self.driver.find_element(by, locator)
        return result

    def finds(self, by, locator=None):
        if locator is None:
            return self.driver.find_elements(*by)
        else:
            return self.driver.find_elements(by, locator)


    #根据传入的文本进行滚动查找
    def find_by_scroll(self, text):
        return self.driver.find_element(MobileBy.ANDROID_UIAUTOMATOR,
                                        'new UiScrollable(new UiSelector()'
                                        '.scrollable(true).instance(0))'
                                        '.scrollIntoView(new UiSelector()'
                                        f'.text("{text}").instance(0));')

    #显示等待，作用于局部
    def webdriver_wait(self, by, locator, timeout):
        element = WebDriverWait(self.driver, timeout).until(
            lambda x: x.find_element(by,locator))
        return element

    #对yaml文件中的测试步骤进行解析
    def step(self,path,name):
        with open(path,encoding='utf-8') as f:
            steps=yaml.safe_load(f)[name]
        raw = json.dumps(steps)
        for key, value in self._params.items():
            raw = raw.replace('${' + key + '}', value)
        steps = json.loads(raw)
        for step in steps:
            if 'action' in step.keys():
                action = step['action']
                if 'click' == action:
                    self.find(step['by'],step['locator']).click()
                if 'sendkey' == action:
                    self.find(step['by'],step['locator']).send_keys(step['value'])
                if 'webdriver_wait' == action:
                    self.webdriver_wait(step['by'],step['locator'],step['time'])
                if 'sleep'== action:
                    time.sleep(step['time'])
                if 'press_release' == action:
                    self.press_release(step['w_percent'],step['hf_percent'],step['hl_percent'])
                if 'gettext' == action:
                    return self.find(step['by'],step['locator']).text


    #隐式等待，作用于全局
    def set_implicitly_wait(self,num):
        self.driver.implicitly_wait(num)

    #截图
    def screenshot(self, path):
        self.driver.save_screenshot(path)

    #根据屏幕分辨率进行滑屏操作，传入滑屏比例
    def press_release(self, w_percent, hf_percent, hl_percent):
        window = self.driver.get_window_rect()
        phone_width = window['width']
        phone_height = window['height']
        width = int(phone_width * w_percent)
        heightf = int(phone_height * hf_percent)
        heightl = int(phone_height * hl_percent)
        action = TouchAction(self.driver)
        action.press(x=width, y=heightf).move_to(x=width, y=heightl).release().perform()

    #返回上一层
    def back(self):
        self.driver.back()

