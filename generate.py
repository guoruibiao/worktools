#!/usr/bin python
# coding: utf8

import re
import sys
import json
from flask import Flask, request

app = Flask(__name__)

def reg_rules(type):
    s = ''
    if type == 'class':
        s = "function ([a-zA-Z_].*?)\((.*?)\)"
    elif type == 'action':
        s = "\$action == .*?([a-zA-Z_0-9]+).*?"
    return re.compile(s)

def main(path, type):
    matched = []
    with open(path, "r") as f:
        lines = f.readlines()
        for line in lines:
            result = re.findall(reg_rules(type), line)
            try:
                if result:
                    if type == 'class':
                        tempdict = dict(result)
                        matched.append(tempdict)
                    else:
                        matched.append("请求接口名称："+str(result.pop()))
            except:
                continue
        f.close()
    return matched


@app.route('/')
def index():
    return "Push in the file path, get the doc!   :)"

@app.route("/generate", methods=['GET', 'POST'])
def generate_doc():
    path = request.args.get('path')
    type = request.args.get('type')
    result = main(path, type)
    return json.dumps(result)


if __name__ == "__main__":
    app.run(host='localhost', port=80, debug=True)


