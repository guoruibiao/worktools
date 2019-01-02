#!/usr/bin python
#coding:utf8
###############################################
# File Name: clean_tmp.py
# Author: 郭 璞
# mail: marksinoberg@gmail.com
# Created Time: 三  1/ 2 10:43:52 2019
# Description: 清理ctime在一周前的文件 
###############################################
import os
import time
# 待清理目标文件夹，需完整路径
TARGET_FOLDERS = "/tmp"
# 白名单文件，也需要为完整路径
EXCLUDE_SLOTS = [
    "/Users/biao/Downloads/WechatIMG68.jpeg",
    ]

# 返回一周之前的时间戳
def get_weekago_ts():
    return time.time() - 86400 * 7

# 判断一个文件是否过期
def is_expired(fullname):
    expired = False
    if os.path.exists(fullname):
        ctime = os.path.getctime(fullname)
        if ctime < get_weekago_ts():
            expired = True
    return expired

# 全遍历出过期的文件清单
def folder_walk(foldername, ret):
    if os.path.exists(foldername):
        for tp in os.walk(foldername):
            dirpath, dirnames, filenames = tp
            for filename in filenames:
                fullname = dirpath + "/" + filename
                if is_expired(fullname) == True:
                    ret.append(fullname)
            # 开启新一轮遍历
            if dirnames != []:
                for dirname in dirnames:
                    newfoldername = dirpath + "/" + dirname
                    folder_walk(newfoldername, ret)

# 清理文件                    
def clean(fullnames):
    # 过滤掉白名单中的文件
    global EXCLUDE_SLOTS
    fullnames = list(set(fullnames) - set(EXCLUDE_SLOTS))
    for fullname in fullnames:
        os.remove(fullname)
        print("removed {}".format(fullname))

def main():
    global TARGET_FOLDERS
    ret = []
    foldername = TARGET_FOLDERS
    folder_walk(foldername, ret)
    clean(ret)

if __name__ == "__main__":
    main()
