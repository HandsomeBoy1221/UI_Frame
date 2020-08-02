import yaml
from appium.webdriver.common.mobileby import MobileBy
from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from UI_Frame.page.handle_black import handle_black


class BasePage:
    _black_list = [
        (By.XPATH, "//*[@resource-id='com.xueqiu.android:id/iv_close']")
    ]
    _max_err_num = 3
    _error_num = 0

    def __init__(self,driver:WebDriver=None):
        self.driver=driver

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


    def find_by_scroll(self, text):
        return self.driver.find_element(MobileBy.ANDROID_UIAUTOMATOR,
                                        'new UiScrollable(new UiSelector()'
                                        '.scrollable(true).instance(0))'
                                        '.scrollIntoView(new UiSelector()'
                                        f'.text("{text}").instance(0));')

    def webdriver_wait(self, locator, timeout=10):
        element = WebDriverWait(self.driver, timeout).until(
            lambda x: x.find_element(*locator))
        return element


    def step(self,path,name):
        with open(path,encoding='utf-8') as f:
            steps=yaml.safe_load(f)[name]
        for step in steps:
            if 'action' in step.keys():
                action = step['action']
                if 'click' == action:
                    self.driver.find_element(step['by'],step['locator']).click()
                if 'sendkey' == action:
                    self.driver.find_element(step['by'],step['locator']).send_keys(step['value'])


    def set_implicitly_wait(self,num):
        self.driver.implicitly_wait(num)


