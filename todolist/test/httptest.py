# coding: utf8

# @Author: 郭 璞
# @File: httptest.py                                                                 
# @Time: 2018/2/21                                   
# @Contact: 1064319632@qq.com
# @blog: http://blog.csdn.net/marksinoberg
# @Description: 
import requests

url = "http://localhost:8888/all"
payload = {
    "todoid": 8,
    "status": 1,
}
response = requests.get(url, data=payload)
print(response.text)