# coding: utf8

# @Author: 郭 璞
# @File: finder.py                                                                 
# @Time: 2017/9/1                                   
# @Contact: 1064319632@qq.com
# @blog: http://blog.csdn.net/marksinoberg
# @Description: 方便平时各种简短信息查找的个人工具。
# 初步设想有两种实现，一种是借助redis等外部存储；另一种是使用whoosh这样的全文检索引擎。
# 后者相对而言在这个场景下不是很适合,打算做成模糊查询性质，对查询结果评分排序输出。

import redis
import sqlite3
import pymysql
import pymongo
import whoosh


class SearcherBase(object):
    def __init__(self):
        pass


class RedisSearcher(SearcherBase):
    """
    根据简短信息特点，默认使用hash数据结构作为存储支撑。
    """
    def __init__(self, cfg={}):
        host = "localhost" if cfg['host'] else cfg['host']
        port = 6379 if cfg['port'] else int(cfg['port'])
        db = int(cfg['db']) if cfg['db'] else 0
        self.r = redis.StrictRedis(host=host, port=port, db=db)

    def search(self, hashkey, field=""):
        if field == "":
            temp = self.r.hgetall(hashkey)
            result = {}
            for key in temp.keys():
                result[key.decode('utf8')] = temp[key].decode('utf8')
            return result
            return {key.decode('utf8'):value.decode('utf8') for key, value in self.r.hgetall(hashkey) }
        else:
            value = self.r.hget(hashkey, field)
            return {field: value.decode('utf8')} if value!=None else {field: ""}

    def save(self, hashkey, items={}):
        for item in items.keys():
            self.r.hset(hashkey, item, items[item])

    def remove(self, hashkey, field=""):
        if field == "":
            self.r.delete(hashkey)
        else:
            self.r.hdel(hashkey, field)
    def update(self, hashkey, items={}):
        self.save(hashkey, items)


class DbSearcher(SearcherBase):
    """
    打算对关系型数据库和非关系型数据库都进行支持。可以通过dbtype进行区别对待。
    """
    def __init__(self, cfg={}):
        pass

class MySQLSearcher(DbSearcher):

    def __init__(self, cfg={}):
        # type = cfg.get("dbtype", "")
        host = cfg.get("host", "localhost")
        port = cfg.get("port", 3306)
        user = cfg.get("user", "root")
        password = cfg.get("password", "mysql")
        dbname = cfg.get("dbname", "test")
        self.conn = pymysql.connect(host=host, port=port, user=user, passwd=password, db=dbname, charset="utf8")
        # 对表的存在性进行判断，有则无需创建，否则需要进行创建
        self.createtb = """
                create table lists(
                id int(11) not null primary key auto_increment,
                field VARCHAR(255),
                host VARCHAR (255),
                port INT (11),
                user VARCHAR(255),
                password VARCHAR(255),
                dbname VARCHAR(255),
                UNIQUE KEY index_field(`field`)
                );
                """
        cursor = self.conn.cursor()
        sql = "select `TABLE_NAME` from `INFORMATION_SCHEMA`.`TABLES` where TABLE_SCHEMA='{}' and TABLE_NAME='lists'".format(dbname)
        rs = cursor.execute(sql)
        if rs==0:
            cursor.execute(self.createtb)
        cursor.close()

    def searchOne(self, key):
        sql = "SELECT * FROM lists WHERE field='{}'".format(key)
        cursor = self.conn.cursor()
        er = cursor.execute(sql)
        rs = cursor.fetchone()
        cursor.close()
        return rs if er else ""
    def searchAll(self):
        sql = "SELECT * FROM lists"
        cursor = self.conn.cursor()
        cursor.execute(sql)
        rs = cursor.fetchall()
        cursor.close()
        return rs

    def save(self, items=[]):
        sql = "insert into lists(field, host, port, user, password, dbname) values"
        for item in items:
            sql += "('{}', '{}', {}, '{}', '{}', '{}'),".format(item.get('field'), item.get('host'), int(item.get('port')), item.get('user'), item.get('password'), item.get('dbname'))
        sql = sql.rstrip(",")
        cursor = self.conn.cursor()
        cursor.execute(sql)
        cursor.close()

    def update(self, key, item={}):
        sql = "update lists set host='{}', port={}, user='{}', password='{}', dbname='{}'".format(item.get('host'), int(item.get('port')), item.get('user'), item.get('password'), item.get('dbname'))
        cursor = self.conn.cursor()
        cursor.execute(sql)
        cursor.close()

    def remove(self, key):
        sql = "delete from lists where field='{}'".format(key)
        cursor = self.conn.cursor()
        cursor.execute(sql)
        cursor.close()








class SQLiteSearcher(DbSearcher):
    def __init__(self, cfg={}):
        pass

class MongoSearcher(DbSearcher):

    def __init__(self, cfg={}):
        pass

class WhooshSearcher(SearcherBase):
    def __init__(self, cfg={}):
        """
        建立索引条件
        :param cfg:
        """
        pass


if __name__ == '__main__':
    cfg = {"host": "localhost", "db": 1, "port": 6379}
    rs = RedisSearcher(cfg=cfg)
    items = {
        "name": "郭璞",
        "age": 21,
        "address": "北京市朝阳区",
        "home": "我的家在东北，松花江上。。。",
        "school": "大连理工大学",
    }
    #rs.save("hashkey", items)
    #print("存储完毕")
    #rs.update("hashkey", {"name": "marksinoberg", "blog": "http://blog.csdn.net/marksinoberg"})
    #print("更新完毕")
    # name = rs.search("hashkey", 'home')
    # print(name)
    # rs.remove('hashkey', 'name')
    # name = rs.search("hashkey")
    # print(name)
    # cfg = {}
    items = [{"field": "test", "host": "localhost", "port": 3306, "user": "root", "password": "mysql", "dbname": "test"}]
    #
    ms = MySQLSearcher(cfg=items[0])
    # ms.save(items)
    result = ms.searchOne('test')
    print(result)
    # result = ms.searchAll()
    # print("获取到的结果为：")
    # print(result)
    items[0]['dbname'] = "mysql"
    ms.update('test', items[0])
    result = ms.searchOne('test')
    print(result)




