import os
import signal
import subprocess

import pytest

#pytest特性，conftest文件会自动执行，将测试过程的视频保存
@pytest.fixture(scope="class", autouse=True)
def record():
    cmd = "scrcpy --no-display --record ../result/tmp.mp4"
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    yield
    os.kill(p.pid, signal.CTRL_C_EVENT) #windows结束方式
    #os.kill(p.pid, signal.SIGTERM) #mac结束方式