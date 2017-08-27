# coding: utf8

# @Author: 郭 璞
# @File: sqlhelper.py                                                                 
# @Time: 2017/8/26                                   
# @Contact: 1064319632@qq.com
# @blog: http://blog.csdn.net/marksinoberg
# @Description: 执行SQL语句的帮手

import configparser
import argparse
import pymysql
import sys
import prettytable
from prettytable import PrettyTable
from colorama import init, Fore, Back, Style


class Configer(object):
    def __init__(self, path='./db_config.ini'):
        self.path = path
        self.cf = configparser.ConfigParser()
        self.cf.read(filenames=path)
        self.section = self.cf.sections().pop()
        self.mysqlcfg = self.cf.options(self.section)

    def setItem(self, name, value):
        if name in self.cf.options(self.section):
            self.cf.set(self.section, str(name), str(value))
        else:
            print("无效的配置项：{}".format(name))
        with open(self.path, 'w') as file:
            self.cf.write(file)
            file.close()
    def setItems(self, items={}):
        for key in items:
            self.setItem(key, items[key])
        with open(self.path, 'w') as file:
            self.cf.write(file)
            file.close()

    def getItem(self, name):
        self.cf.get(self.section, name)

    def getItems(self):
        items = self.cf.items(self.section)
        return {key: value for key, value in items}


class SQLHelper(object):
    def __init__(self, cfg={}):
        self.conn = pymysql.connect(host=cfg['host'], port=int(cfg['port']),
                                    user=cfg['user'], passwd=cfg['password']
                                    , db=cfg['dbname'], charset='utf8')

    def select(self, sql, single=False):
        cursor = self.conn.cursor()
        effected_rows = cursor.execute(sql)
        fields = cursor.description
        if single:
            rs = cursor.fetchone()
        else:
            rs = cursor.fetchall()
        cursor.close()
        return (effected_rows, fields, rs)


class Table(object):
    def __init__(self, fields, rs):
        if rs is None:
            print("请先赋予工具结果集！")
        else:
            self.desc = [Style.BRIGHT + str(th[0]) for th in list(fields)]
            self.table = PrettyTable(self.desc)
            init(autoreset=True)
            for index, tr in enumerate(rs):
                if index % 2 == 0:
                    tr = [Fore.LIGHTGREEN_EX + str(td) for td in list(tr)]
                else:
                    tr = [Fore.YELLOW + str(td) for td in list(tr)]
                self.table.add_row(tr)

    def showTable(self):
        return self.table


def main():
    description = """
        sqlhelper-0.0.1一个不用登陆SQL窗口的命令行执行器，更少操作，更专注！首次使用请预先配置数据库连接信息。
         选择一： 使用命令行的方式，具体可以参考-h 或者 -e True选项；
         选择二： 在sqlhelper.py同级目录下新建db_config.ini文件。按照[mysql]下对host,port,user,password,dbname等进行配置。
    """
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-r", "--sql", help='将要被执行的完整的SQL语句。')
    parser.add_argument("-e", "--example", help="关于SQLhelper的几个典型示例。三个选项run,config,all对应了运行SQL，配置数据库连接信息，和查看所有示例三个行为！", choices=['run', 'config', 'all'])
    parser.add_argument('-s', "--set", nargs='+', help="初始化数据库连接信息，可以随意设置需要的项。默认host=localhost port=3306 ")
    arguments = parser.parse_args()

    if arguments.example:
        rs = (
            (1, "python sqlhelper.py -h"),
            (2, "python sqlhelper.py -e run/config"),
            (3, 'python sqlhelper.py -r "select * from tablename where case and case order by field ..."'),
            (4, 'python sqlhelper.py -s [host=ip [port=portnumber [user=user [password=password [dbname=dbname]]]]]')
        )
        fields = ("编号", "示例")
        if arguments.example == "run":
            table = Table(fields=fields, rs=(rs[2],))
        elif arguments.example == "config":
            table = Table(fields=fields, rs=(rs[3],))
        else:
            table = Table(fields=fields, rs=rs)
        table.align = "l"
        print(table.showTable())
    else:
        pass
    sql = arguments.sql
    if arguments.set:
        # 需要进行配置更改
        cfg = {key: value for key, value in [item.split("=") for item in arguments.set]}
        # 将持久化信息持久化到本地
        cfger = Configer()
        cfger.setItems(cfg)
        print("成功配置数据库连接信息！")
    if sql:
        cfg = Configer().getItems()
        helper = SQLHelper(cfg=cfg)
        er, fields, rs = helper.select(sql)
        if er:
            table = Table(fields, rs)
            table.align='l'
            print(table.showTable())
        else:
            print("SQL执行出错了！")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
