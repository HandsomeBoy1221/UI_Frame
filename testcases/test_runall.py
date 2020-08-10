import sys

print(sys.path.append('../..'))

import time

import pytest
import yaml

from UI_Frame.page.app import App

with open('../datas/test_runall.yaml',encoding='utf-8') as f:
    gotomaindatas=yaml.safe_load(f)['test_gotomain']
with open('../datas/test_runall.yaml',encoding='utf-8') as f:
    gotoadatas=yaml.safe_load(f)['test_a']

class TestRunAll():
    def setup_class(self):
        self.app=App()
        self.main=self.app.start().goto_main()

    def teardown_class(self):
        self.app.stop()

    def teardown(self):
        self.app.restart()

    @pytest.mark.parametrize('name',gotomaindatas)
    def test_gotomain(self,name):
        self.main.goto_search().search()
        print(name)
        time.sleep(2)

    @pytest.mark.parametrize('name',gotoadatas)
    def test_a(self,name):
        print(name)
        time.sleep(2)
        pass