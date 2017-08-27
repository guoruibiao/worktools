# coding: utf8

# @Author: 郭 璞
# @File: exectool.py                                                                 
# @Time: 2017/8/26                                   
# @Contact: 1064319632@qq.com
# @blog: http://blog.csdn.net/marksinoberg
# @Description: 调试助手工具

import subprocess
import requests
cmd = ""
p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

while True:
    data = p.stdout.readline()
    if data == b'':
        if p.poll() is not None:
            break
        else:
            print(data)
