#!/usr/bin python
#coding: utf8
import sys
reload(sys)
sys.setdefaultencoding("utf8")
import re
import os
from colorcmd import Color, Style, Enhancer


def find(filepath, keyword):
    if os.path.isdir(filepath):
        # 明天做下递归版本
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
            wrappedword = Enhancer.mix(keyword, Color.BLACK_DEEPGREEN, Style.HIGHLIGHT+Style.UNDERLINE+Style.BLINK)
            tmp = {"number": counter, "line":line.rstrip("\n").replace(keyword, wrappedword)}
            result.append(tmp)
    return result

def pretty_print(filepath, rows):
    for row in rows:
        if row is not None or row != []:
            print "-------"*5 + filepath + "-------"*5
            print "Line: {}\t {}".format(row['number'], row['line'])
filepath = sys.argv[1]
keyword = sys.argv[2]
rows = find(filepath, keyword)
pretty_print(filepath, rows)
