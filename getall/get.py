# coding: utf8

# @Author: 郭 璞
# @File: get.py                                                                 
# @Time: 2017/9/2                                   
# @Contact: 1064319632@qq.com
# @blog: http://blog.csdn.net/marksinoberg
# @Description: 用redis实现一个类似于tmux管理简短信息的工具。
import redis
import sys
from flask import Flask, request

class RedisHelper(object):
    def __init__(self, cfg={}):
        host = cfg.get("host", "localhost")
        port = int(cfg.get('port', 6379))
        db = int(cfg.get("db", 0))
        self.r = redis.StrictRedis(host=host, port=port, db=db)

    def search(self, hashkey, field=""):
        if field == "":
            temp = self.r.hgetall(hashkey)
            result = {}
            for key in temp.keys():
                result[key.decode('utf8')] = temp[key].decode('utf8')
            return result
            return {key.decode('utf8'): value.decode('utf8') for key, value in self.r.hgetall(hashkey)}
        else:
            value = self.r.hget(hashkey, field)
            return {field: value.decode('utf8')} if value != None else {field: ""}

    def searchAll(self):
        """
        重操作，慎重用。当然了，数据量小的话，无所谓。
        :return:
        """
        allkeys = self.r.keys("*")
        hashkeys = []
        for key in allkeys:
            if self.r.type(key) == b'hash':
                hashkeys.append(key.decode('utf8'))
        result = []
        for key in hashkeys:
            result.append(self.search(key))
        return result

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


class ConsoleHelper(object):
    """
    终端内打印格式良好的数据信息。
    """

    def __init__(self, cfg={}):
        self.helper = RedisHelper(cfg=cfg)

    def log(self, key, field=''):
        if field:
            result = self.helper.search(key, field)
            print("单项查询，{}中{}的内容为：{}".format(key, field, result))
        else:
            print("条目查询，{}下的所有存储结果为：".format(key))
            result = self.helper.search(key)
        print(result)


    def logall(self):
        result = self.helper.searchAll()
        print("即将打印全量数据，请有选择性的复制！")
        for index, item in enumerate(result):
            print("序号：{}, 内容为：{}".format(index+1, item))

class WebHelper(object):
    """
    暂停更新
    """
    def __init__(self):
        self.app = Flask(__name__)

    def run(self):
        print("本地服务已开启，请用浏览器打开 http://localhost:8888 查看服务详情！")
        self.app.run(host='localhost', port=8888, debug=True)

app = WebHelper().app

@app.route("/")
def index():
    details = """
    <ul>
      <li><a href='#'>dasdsa</a></li>
      <li><a href='#'>dasdsa</a></li>
      <li><a href='#'>dasdsa</a></li>
      
    </ul>
    """
    return details


if __name__ == '__main__':
    cfg = {'db': 1}
    # helper = RedisHelper(cfg=cfg)
    # items = {"host": "127.0.0.1", "port": 6379, "db": 1}
    # helper.save('localredis', items)
    # result = helper.search('test')
    # print(result)
    # results = helper.searchAll()
    # print(results)
    ConsoleHelper(cfg).log('test')
    ConsoleHelper(cfg).logall()
    # wh = WebHelper()
    # wh.run()
