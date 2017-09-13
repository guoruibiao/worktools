#!/usr/bin python
# coding: utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# 将MySQL中某些表的数据转化成CSV或者Excel表
import re
import csv
import pymysql
import argparse

class Configer(object):
    """
    根据给定路径下的关于数据库的配置文件，解析出符合要求的数据库连接信息
    """
    def __init__(self, filepath="./alias.list"):
        with open(filepath, 'r') as f:
            data = f.readlines()
            f.close()
        self.data = [str(item) for item in data if len(item.strip())!=0]

    def getConfigByName(self, alias):
        for item in self.data:
            dbname = str(item.split("=")[0]).split(" ")[1]
            if alias in dbname:
                return self._parse(item)
            else:
                continue

    def _parse(self, item):
        name, config = item.split("=")
        host = "192.168.1.{}".format(self._split_host(name))
        config = config.lstrip("'").rstrip("'\n").split(" ")
        port = config[2].lstrip("-P")
        user = config[3].lstrip("-u")
        password = config[-1]
        return {
            "host": host,
            "port": port,
            "user": user,
            "password": password,
        }

    def _split_host(self, name):
        reg = re.compile("\d+")
        return re.findall(reg, name)[0]


class DbHelper(object):
    """
    根据Configer返回的数据库配置信息连接数据库，从而可以实现数据的读写。
    """
    def __init__(self, cfg={}, dbname=""):
        self.conn = pymysql.connect(host=cfg.get("host"), port=int(cfg.get("port")), user=cfg.get("user"), passwd=cfg.get("password"), db=dbname, charset="utf8")

    def read(self, sql):
        cursor = self.conn.cursor()
        try:
            effected_rows = cursor.execute(sql)
            if effected_rows:
                description = cursor.description
                resultset = cursor.fetchall()
                return (description, resultset)

        except:
            cursor.close()
        finally:
            cursor.close()

class CSVHelper(object):
    """
    把从数据库查询到的结果集保存到数据库， 包括对header的处理。
    """
    def __init__(self, savepath="./target.csv"):
        self.writer = csv.writer(file(savepath, 'wb'))


    def write(self, description, resultset):
        fields = self.parseFields(description)
        self.writer.writerow(fields)
        for row in resultset:
            self.writer.writerow(list(row))
        print "数据已写入csv文件!"

    def parseFields(self, description):
        fields = []
        for item in description:
            fields.append(item[0])
        return fields


def main():
    tooldescription = """
    datatransfer.py 是一款针对MySQL数据库中导出数据的工具。依赖于alias.list文件，具体的格式为：
        alias dbname='mysql -h ip -Pport -uname -ppassword'
    参数列表：
      必写参数：
        -d   dbalias            用于指定对数据库在alias.list中的别名，方便获取配置信息。
        -t   target             用于指定对那个数据库进行数据迁移操作。
        -r   sql-statement      具体用于执行的SQL语句。
        -o   output             用于指定转换后的CSV文件的存储路径。
      可选参数：
        -c   config-file-path   指定alias.list数据库链接配置文件的路径
    案例：
        python datatransfer.py -c your-alias.list-path -d 127 -t zuitaoktv  -r "select * from artist where artisst_name='周杰伦'" -o path/xx.csv
    """
    parser = argparse.ArgumentParser(description=tooldescription)
    parser.add_argument("-d", "--dbalias", help="指定要连接的数据库名称，代号可以是数据库的编号，比如192.168.1.127的编号就是127, 即： -d 127")
    parser.add_argument("-t", "--target", help="指定要对哪个数据库进行操作, 如: -t zutaoktv")
    parser.add_argument("-r", "--sql", help="将要被执行的SQL语句， 如: select * from tablename where ...")
    parser.add_argument("-o", "--output", help="指定转换到的CSV文件的输出路径, 如: -o /tmp/log/xx.csv")
    # 可选参数，
    parser.add_argument("-c", "--config", help="指定alias.list的配置文件的路径")

    args = parser.parse_args()

    # 准备数据库配置信息
    configer = Configer(filepath=args.config)
    cfg = configer.getConfigByName(args.dbalias)
    dbhelper = DbHelper(cfg=cfg, dbname=args.target)
    ds, rs = dbhelper.read(args.sql)
    #print ds
    csvhelper = CSVHelper(savepath=args.output)
    csvhelper.write(ds, rs)




if __name__ == '__main__':
    # configer = Configer(filepath="./alias.list")
    # cfg = configer.getConfigByName(alias="guo127")
    # cfg = {
    #     "host": "localhost",
    #     "port": 3306,
    #     "user": "root",
    #     "password": "guoruibiao"
    # }
    # helper = DbHelper(cfg=cfg, dbname="mysql")
    # description, rs = helper.read("select Host, Db, User from db")
    # csvhelper = CSVHelper(savepath="./target.csv")
    # csvhelper.write(description, rs)
    main()
