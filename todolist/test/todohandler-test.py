# coding: utf8

# @Author: 郭 璞
# @File: todohandler-test.py                                                                 
# @Time: 2018/2/21                                   
# @Contact: 1064319632@qq.com
# @blog: http://blog.csdn.net/marksinoberg
# @Description: 
from todolist.app.service import Todo

th = Todo()



# result = th.get_all_unfinished()
# print(result)
# result = th.get_all_finished()
# print(result)
# result = th.update_desc_by_id(5, "")
# print(result)

result = th.get_detail_by_id(1)
print(result)
# result = th.get_todays_list()
# print(result)
# result = th.add_newone("通过代码再来添加一个新的记录")
# print(result)

# result = th.update_status_by_id(1, 0)
# print(result)
# result = th.update_status_by_id(1, 1)
# print(result)
# result = th.update_status_by_id(1, 0)
# print(result)