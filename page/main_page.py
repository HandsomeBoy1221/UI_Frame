import time

from UI_Frame.page.base_page import BasePage


class MainPage(BasePage):
    def goto_search(self):
        self.step('../steps/main_page.yaml','goto_search')
        time.sleep(3)
        return self

    def search(self):
        self.step('../steps/main_page.yaml', 'search')
        return self