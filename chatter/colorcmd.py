#!/usr/bin python
# coding: utf8
import sys
reload(sys)
sys.setdefaultencoding("utf8")
"""
# 之前用过一个colorama的库，挺好用的，但是有一个缺点就是有时候init(autoreset=True)并不很好使，究其原因，还是设计层面的问题
于是我打算使用“包装”的思想，来做一个更好用一点的出来。
"""

class Color(object):
    CLEAR = "\33[0m"
    # 字体颜色 前景色
    FORE_BLACK = "\33[30m"
    FORE_RED = "\33[31m"
    FORE_GREEN = "\33[32m"
    FORE_YELLOW = "\33[33m"
    FORE_BLUE = "\33[34m"
    FORE_PURPLE = "\33[35m"
    FORE_DEEPGREEN = "\33[36m"
    FORE_WHITE = "\33[37m"
    # 背景色
    BACK_BLACK = "\33[40"
    BACK_RED = BACK_DEEPRED = "\33[41m"
    BACK_GREEN = "\33[42m"
    BACK_YELLOW = "\33[43m"
    BACK_BLUE = "\33[44m"
    BACK_PURPLE = "\33[45m"
    BACK_DEEPGREEN = "\33[46m"
    BACK_WHITE = "\33[47m"
    # 黑底彩色
    BLACK_BLACK = "\33[90m"
    BLACK_RED = BLACK_DEEPRED = "\33[91m"
    BLACK_GREEN = "\33[92m"
    BLACK_YELLOW = "\33[93m"
    BLACK_BLUE = "\33[94m"
    BLACK_PURPLE = "\33[95m"
    BLACK_DEEPGREEN = "\33[96m"
    BLACK_WHITE = "\33[97m"
    """
    颜色相关工具类
    """
    def __init__(self):
        pass


class Style(object):
    CLEAR = "\33[0m"
    HIGHLIGHT = "\33[1m"
    UNDERLINE = "\33[4m"
    BLINK = "\33[5m"
    REVERSE = "\33[7m"
    BLANKING = "\33[8m"
    """
    样式相关，前景色，背景色,加粗，下划线等
    """
    def __init(self):
        pass

class Enhancer(object):
    """
    曾经有一个tag的交叉叠加，给了我这个思路。目标是做成一个无限叠加的增强品。
    """
    def __init__(self):
        pass

    @staticmethod
    def highlight(text="", color=Color.FORE_RED, style=Style.CLEAR):
        return Style.HIGHLIGHT + style + color + text + Style.CLEAR

    @staticmethod
    def mix(text, color=Color.CLEAR, style=Style.CLEAR, highlight=False):
        return style + color + text + Style.CLEAR
if __name__ == "__main__":
    #print "\33[5m"+Color.FORE_GREEN+"Hello World!"+"\33[0m"
    text = "郭璞"
    print Enhancer.highlight(text, Color.BACK_GREEN, Style.BLINK)
    print Enhancer.mix("what a amazing colorama!", Color.BLACK_PURPLE, Style.UNDERLINE+Style.HIGHLIGHT+Style.BLINK)

