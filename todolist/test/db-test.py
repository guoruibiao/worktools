# coding: utf8

# @Author: 郭 璞
# @File: db-test.py                                                                 
# @Time: 2018/2/21                                   
# @Contact: 1064319632@qq.com
# @blog: http://blog.csdn.net/marksinoberg
# @Description: 
from todolist.app.db import DbHelper

dh = DbHelper()

# rs = dh.query("select * from todo_detail", False)
# print(rs)
rs = dh.save("update todo_detail set finish_time=now() where id=%s", (2))
print(rs)
rs = dh.save("insert into todo_detail(description) values(%s)", ("测试插入一条记录"))
print(rs)