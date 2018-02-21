# coding: utf8

# @Author: 郭 璞
# @File: config-test.py                                                                 
# @Time: 2018/2/21                                   
# @Contact: 1064319632@qq.com
# @blog: http://blog.csdn.net/marksinoberg
# @Description: 
from todolist.app import service
if __name__ == '__main__':
    cp = service.ConfigParser(filepath="../todo.cfg.json")
    print(cp.get_db_config())
    print(cp.get_runtime_config())
    print(cp.get_debug_config())