import logging

import allure
from selenium.webdriver.common.by import By


#自定义黑名单装饰器



def handle_black(func):
    logging.basicConfig(level=logging.INFO)

    def wrapper(*args, **kwargs):
        from UI_Frame.page.base_page import BasePage
        instance: BasePage = args[0]
        try:
            logging.info("run " + func.__name__ + "\n args: \n" + repr(args[1:]) + "\n" + repr(kwargs))
            element = func(*args, **kwargs)
            _error_num = 0
            return element
        except Exception as e:
            instance.screenshot("../result/tmp.png")
            with open("../result/tmp.png", "rb") as f:
                content = f.read()
            allure.attach(content, attachment_type=allure.attachment_type.PNG)
            logging.error("该元素没找到, 进入黑名单查看")
            # 如果没找到，就进行黑名单处理
            if instance._error_num > instance._max_err_num:
                # 如果 erro 次数大于指定指，清空 error 次数并报异常
                instance._error_num = 0
                raise e
            instance._error_num += 1
            for ele in instance._black_list:
                # 对黑名单进行点击
                eles = instance.finds(ele)
                if len(eles) > 0:
                    eles[0].click()
                    return wrapper(*args, **kwargs)
            raise ValueError("找不到该元素，且不在黑名单中")

    return wrapper