# coding: utf8

# @Author: 郭 璞
# @File: index.py.py                                                                 
# @Time: 2018/2/21                                   
# @Contact: 1064319632@qq.com
# @blog: http://blog.csdn.net/marksinoberg
# @Description: 总入口，一方面处理页面，一方面负责dispatch接口相关请求
from flask import Flask, request,render_template
from flask_restful import Api, Resource
from service import *

app = Flask(__name__)
api = Api(app)

@app.route("/", methods=["POST", "GET"])
def index():
    return render_template("index.html")

@app.route("/detail/<int:todoid>", methods=["POST", "GET"])
def detail(todoid=0):
    todo = Todo()
    data = todo.get_detail_by_id(todoid)
    return render_template("detail.html", schema=data[1], data=data[2])

# URL路由规则
api.add_resource(HelloWorld, "/hello")
# api.add_resource(DetailHandler, "/detail/<int:todoid>")
api.add_resource(DailyHandler, "/daily")
api.add_resource(YesterdayHandler, "/yesterday")
api.add_resource(WeekHandler, "/week")
api.add_resource(AddHandler, "/add")
api.add_resource(UpdateDescHandler, "/updatedesc")
api.add_resource(UpdateStatusHandler, "/updatestatus")
api.add_resource(AllFinishedHandler, "/allfinished")
api.add_resource(AllUnfinishedHandler, "/allunfinished")
api.add_resource(AllHandler, "/all")
if __name__ == "__main__":
    cp = ConfigParser(filepath="./todo.cfg.json")
    runtimecfg = cp.get_runtime_config()
    app.run(host=runtimecfg["host"], port=runtimecfg["port"], debug=runtimecfg["debug"])
