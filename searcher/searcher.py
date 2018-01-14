#!/usr/bin python
#coding: utf8
import sys
reload(sys)
sys.setdefaultencoding("utf8")
import re
import os
from colorcmd import Color, Style, Enhancer
from prettytable import PrettyTable

class Table(object):
    """
    借助PrettyTable实现类似于MySQL的命令行的输出效果
    """
    def __init__(self, fields, rows):
        if rows is None:
            print("empty set(0.00Sec)")
        else:
            self.desc = [Enhancer.highlight(str(th), color=Color.BLACK_RED, style=Style.BLINK) for th in list(fields)]
            self.table = PrettyTable(self.desc)
            for index, tr in enumerate(rows):
                if index % 2 ==0:
                    tr = [Enhancer.mix(str(td), color=Color.FORE_GREEN) for td in list(tr)]
                else:
                    tr = [str(td) for td in list(tr)]
                self.table.add_row(tr)
    def show(self):
        return self.table

def find(filepath, keyword):
    if os.path.isdir(filepath):
        # 明天做下递归版本
        return []
    if ".svn" in filepath:
        return []
    result = []
    with open(filepath, 'r') as file:
        lines = file.readlines()
        file.close()
        # 遍历每一行，读取包含关键字的行，并进行临时存储，用于后续美化输出
    counter = 0
    for line in lines:
        counter += 1
        if keyword.lower() in line.lower():
            wrappedword = Enhancer.mix(keyword, Color.BACK_DEEPGREEN, Style.HIGHLIGHT+Style.UNDERLINE+Style.BLINK)
            tmp = {"number": counter, "line":line.rstrip("\n").replace(keyword, wrappedword)}
            #result.append(tmp)
            result.append((filepath, counter, line.rstrip("\n").replace(keyword, wrappedword)))
    return result

def pretty_print(filepath, rows):
    for row in rows:
        if row is not None or row != []:
            print "-------"*5 + filepath + "-------"*5
            print "Line: {}\t {}".format(row['number'], row['line'])
filepath = sys.argv[1]
keyword = sys.argv[2]
rows = find(filepath, keyword)
fields = ('文件名', '行号', '详细内容')
tb = Table(fields, rows)
if rows != []:
    print tb.show()
#pretty_print(filepath, rows)
