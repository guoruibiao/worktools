# coding: utf8

# @Author: 郭 璞
# @File: service.py                                                                 
# @Time: 2018/2/21                                   
# @Contact: 1064319632@qq.com
# @blog: http://blog.csdn.net/marksinoberg
# @Description: 具体的业务处理逻辑，多个handler分别处理不同的业务请求

import json
import pymysql
from flask_restful import Resource
from flask import request, render_template
import datetime

class DateEncoder(json.JSONEncoder):
    """
    解决使用pymysql拿到的数据值中有datetime类型导致的错误
    """
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)


class DbHelper(object):
    """
    python下的MySQL工具类
    """

    def __init__(self):
        # 加载问题，导致路径其实是发生了变化的
        cp = ConfigParser(filepath="todo.cfg.json")
        self.dbconfigs = cp.get_db_config()
        self.conn = pymysql.connect(
                host=self.dbconfigs["host"], port=self.dbconfigs["port"], user=self.dbconfigs["user"],
                passwd=self.dbconfigs["password"],
                db=self.dbconfigs['dbname'], charset="utf8"
        )

    def query(self, sql="", single=True):
        cursor = self.conn.cursor()
        effected_rows = cursor.execute(sql)
        fields = cursor.description
        if single:
            rs = cursor.fetchone()
        else:
            rs = cursor.fetchall()
        cursor.close()
        # 另类的XXX不能被默认的json库序列化的问题
        rs = json.dumps(rs, cls=DateEncoder)
        rs = json.loads(rs)
        return (effected_rows, fields, rs)

    def save(self, sql="", params=()):
        """
        一定要做好防止SQL注入的处理
        :param sql: 带有占位符的SQL语句
        :param params: 元组类型
        """
        cursor = self.conn.cursor()
        effected_rows = cursor.execute(sql, params)
        # 神奇，看来下次这块要注意一下了
        self.conn.commit()
        cursor.close()
        return True if effected_rows>0 else False



class ConfigParser(object):
    """
    配置文件解析，用来反映到具体的执行程序上。
    """
    def __init__(self, filepath="../todo.cfg.json"):
        print(filepath)
        with open(filepath, "r") as cfgfile:
            self.configs = json.load(cfgfile)
            cfgfile.close()


    def get_db_config(self):
        return self.configs['db']

    def get_runtime_config(self):
        return self.configs["runtime"]

    def get_debug_config(self):
        return self.configs["debug"]

class Todo(object):
    """
    restful化请求
    """
    def __init__(self):
        self.dbhelper = DbHelper()

    def get_detail_by_id(self, id=0):
        return self.dbhelper.query("select * from todo_detail where id={}".format(id))

    def get_todays_list(self):
        return self.dbhelper.query("select * from todo_detail where to_days(create_time)=to_days(now())", False)

    def get_yesterday_list(self):
        return self.dbhelper.query("select * from todo_detail where to_days(now()) - to_days(create_time) <= 1 order by id desc", False)

    def get_this_week_list(self):
        return self.dbhelper.query("select * from todo_detail where date_sub(curdate(), interval 7 day) < date(create_time) order by id desc ", False)

    def get_all_unfinished(self):
        return self.dbhelper.query("select * from todo_detail where status=0 order by id desc", False)

    def get_all_finished(self):
        return self.dbhelper.query("select * from todo_detail where status=1 order by id desc", False)

    def get_all_desc(self):
        return self.dbhelper.query("select * from todo_detail order by id desc", False)

    def add_newone(self, description=""):
        return self.dbhelper.save("insert into todo_detail(description) values(%s)", (description))

    def update_status_by_id(self, id=0, status=0):
        sql = "update todo_detail set "
        if int(status) == 1:
            sql += str("finish_time=now(), ")
        sql += str("status=%s where id=%s")
        return self.dbhelper.save(sql, (status, id))

    def update_desc_by_id(self, id=0, description=""):
        sql = "update todo_detail set "
        if description != "":
            sql += str("finish_time=now(), ")
        else:
            return False
        sql += str("description=%s where id=%s")
        return self.dbhelper.save(sql, (description, id))

class HelloWorld(Resource):
    """
    看官网的quickstart小例子
    """
    def get(self):
        return {"hello": "world"}
    def post(self):
        args = request.form
        return {"data": args}

class DetailHandler(Resource):
    """
    select 相关
    """
    def get(self, todoid=0):
        todo = Todo()
        data = todo.get_detail_by_id(todoid)
        # print(data)
        # return {"data": data}
        return render_template("detail.html")

class DailyHandler(Resource):
    def get(self):
        todo = Todo()
        data = todo.get_todays_list()
        return {"data": data}

class YesterdayHandler(Resource):
    def get(self):
        todo = Todo()
        data = todo.get_yesterday_list()
        return {"data": data}

class WeekHandler(Resource):
    def get(self):
        todo = Todo()
        data = todo.get_this_week_list()
        return {"data": data}

class AddHandler(Resource):
    def post(self):
        args = request.form
        desc = args.get("description", "")
        todo = Todo()
        todo.add_newone(desc)
        return {"data": True}

class UpdateDescHandler(Resource):
    def post(self):
        args = request.form
        desc = args.get("description", "")
        todoid = args.get("todoid", 0)
        todo = Todo()
        todo.update_desc_by_id(todoid, desc)
        return {"data": True}

class UpdateStatusHandler(Resource):
    def post(self):
        args = request.form
        todoid = args.get("todoid", 0)
        status = args.get("status", 0)
        todo = Todo()
        todo.update_status_by_id(todoid, status)
        return {"data": True}

class AllUnfinishedHandler(Resource):
    def get(self):
        todo = Todo()
        data = todo.get_all_unfinished()
        return {"data": data}
class AllFinishedHandler(Resource):
    def get(self):
        todo = Todo()
        data = todo.get_all_finished()
        return {"data":data}

class AllHandler(Resource):
    """
    倒叙输出所有列表项
    """
    def get(self):
        todo = Todo()
        data = todo.get_all_desc()
        return {"data": data}