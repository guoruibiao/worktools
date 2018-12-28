#coding: utf8
__author__ = "郭 璞"
__email__ = "marksinoberg@gmail.com"
# awesome translator for myself
# Dependency `pbcopy` `pbpaste`

import os
import time
import json
import random
try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

MAX_STRING_LEN = 30

def check(raw):
    """检测格式，对链接类，长度, 是否为纯数字，等添加限制"""
    raw = str(raw).strip(" ").strip("\n")
    if len(raw) > MAX_STRING_LEN:
        return False
    if raw.startswith("http"):
        return False
    return True

def parse(raw):
    url = "http://fanyi.youdao.com/translate?&doctype=json&type=AUTO&i={}".format(raw)
    content = urlopen(url).read()
    jsonstr = json.loads(content)
    return jsonstr['translateResult'][0][0]['tgt'].encode('utf8')

def showalert(raw, parse):
    cmd = """osascript  -e 'display notification "{}" with title "{}\"'""".format(parse, raw)
    os.system(cmd)

lastclipdata = ""
while True:
   print("开始监听...")
   clipdata = os.popen("pbpaste").read()
   if lastclipdata != clipdata and check(clipdata) == True:
       ret = parse(clipdata)
       showalert(clipdata, ret)
       lastclipdata = clipdata
   time.sleep(random.randrange(1,3))




