# coding: utf8

# @Author: 郭 璞
# @File: getrealip.py                                                                 
# @Time: 2017/8/27                                   
# @Contact: 1064319632@qq.com
# @blog: http://blog.csdn.net/marksinoberg
# @Description: 获取本机的真实IP

import requests

def iptest():
    ipservers = [
        "canihazip.com/s",
        "ipinfo.io/ip",
        "icanhazip.com",
        "curlmyip.net",
        "ipecho.net/plain",
        "ifcfg.me",
        "ip-addr.es",
    ]

    for item in ipservers:
        try:
            response = requests.get(url="http://" + item)
        except Exception:
            response = requests.get(url="https://")
        if response.status_code == 200:
            print(response.text)


def geobasedonip():
    geoservers = [
        "ipinfo.io/{}",
        "ipinfo.io/{}/loc",
        "greegeoip.net/csv/{}",
        "freegeoip.net/xml/{}",
        # "greegeoip.net/json/github.com"
    ]
    ip = requests.get("http://ipinfo.io/ip").text
    for item in geoservers:
        try:
            response = requests.get(url="http://"+item.format(ip))
        except Exception:
            response = requests.get(url="https://"+item.format(ip))
        if response.status_code == 200:
            print(response.text)

geobasedonip()