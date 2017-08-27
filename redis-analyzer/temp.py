# coding: utf8

# @Author: 郭 璞
# @File: temp.py                                                                 
# @Time: 2017/8/27                                   
# @Contact: 1064319632@qq.com
# @blog: http://blog.csdn.net/marksinoberg
# @Description:

import redishelper

cfg = {
    "host": "127.0.0.1",
    "port": 6379,
    "db": 0
}
helper = redishelper.RedisHelper(cfg=cfg)

print(helper.getValue('hashkey'))