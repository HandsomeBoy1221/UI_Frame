from appium import webdriver

from UI_Frame.page.base_page import BasePage
from UI_Frame.page.main_page import MainPage

#App启动页，包含APP启动参数，重启，停止，跳转至首页
class App(BasePage):
    def start(self):
        if self.driver==None:
            desired_caps = {}
            desired_caps['platformName'] = 'Android'
            desired_caps['platformVersion'] = '6.0'
            desired_caps['deviceName'] = 'emulator-5554'
            desired_caps["appPackage"] = "com.xueqiu.android"
            desired_caps["appActivity"] = ".view.WelcomeActivityAlias"
            desired_caps['noReset'] = True  # 不清除缓存
            desired_caps['skipDeviceInitialization'] = True  # 跳过安装，权限设置等操作
            desired_caps['unicodeKeyBoard'] = True
            desired_caps['resetKeyBoard'] = True
            self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        else:
            self.driver.launch_app()
        self.driver.implicitly_wait(10)
        return self

    def stop(self):
        self.driver.quit()

    def restart(self):
        self.driver.launch_app()

    def goto_main(self):
        return MainPage(self.driver)