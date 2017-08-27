# coding: utf8

# @Author: 郭 璞
# @File: server.py                                                                 
# @Time: 2017/8/27                                   
# @Contact: 1064319632@qq.com
# @blog: http://blog.csdn.net/marksinoberg
# @Description: 开一个web服务，探查redis内部存储情况

import redishelper
import json
import time
from flask import Flask, request

app = Flask(__name__)
cfg = {
    "host": "localhost",
    "port": 6379,
    "db": 0
}
helper = redishelper.RedisHelper(cfg)


@app.route('/', methods=['GET', 'POST'])
def index():
    keys = helper.getKeys(pattern='*')
    result = "<h1>" + str(time.ctime()) + "</h1>"
    result += "<table border='2px solid'><thead><td>类型</td><td>键名</td><td>大小</td><td>生存时间</td></thead><tbody>"
    for key in keys:
        result += "<tr>"
        result += "<td>" + helper.getType(key).decode('utf8') + "</td>"
        result += "<td><a href='/detect?key=" + key.decode('utf8') + "'>" + key.decode('utf8') + "</a></td>"
        result += "<td>" + str(helper.getLength(key)) + "</td>"
        result += "<td>" + str(helper.getTTL(key)) + "</td>"
        result += "</tr>"
    result += "</tbody></table>"
    # 添加页面自动刷新
    # result += "<script>setTimeout(function(){window.location.reload();}, 3000)</script>"
    return result


@app.route("/detect", methods=["GET", "POST"])
def detect():
    key = request.args.get('key')
    type = helper.getType(key).decode('utf8')
    result = helper.getValue(key)
    if type == "string":
        return result
    elif type == 'list':
        return "\n".join(["<li>" + item.decode('utf8') + "</li>" for item in result])
    elif type == 'hash':
        return json.dumps({key.decode('utf8'): result[key].decode('utf8') for key in result.keys()})
    elif type == 'zset':
        # result = helper.getValue(key, withscores=True)
        print(result)
        result = {key.decode('utf8'): value for key, value in result}
        return json.dumps(result)


if __name__ == "__main__":
    app.run(host='localhost', port=80, debug=True)
