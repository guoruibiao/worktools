#!/usr/bin python
# coding: utf8
# file: .py

import sys

reload(sys)
sys.setdefaultencoding('utf8')
from socket import *
from time import *
import threading

server = socket(AF_INET, SOCK_STREAM)
server.bind(("", 2222))
server.listen(5)

print "server is listening at {}...".format(server.getsockname())
mydict = dict()
mylist = list()

def tellothers(exceptnum, msg):
    for client in mylist:
        if client.fileno() != exceptnum:
            try:
                client.send(str(mydict[exceptnum])+msg.decode('utf8'))
            except:
                pass


def forthread(myconnection, connnum):
    nickname = myconnection.recv(1024).decode('utf8')
    mydict[myconnection.fileno()] = nickname
    mylist.append(myconnection)
    print "connection: {} hash nickname: {}".format(connnum, nickname)
    tellothers(connnum, "【系统提示】{} 进入了聊天室！".format(mydict[connnum]))
    while True:
        try:
            recvmsg = myconnection.recv(1024).decode('utf8')
            if recvmsg:
                print "{}:{}".format(mydict[connnum], recvmsg)
                tellothers(connnum, recvmsg)
        except:
            try:
                mylist.remove(myconnection)
            except:
                pass
            print "{} exit, 当前人数：{}".format(mydict[connnum], len(mylist))
            tellothers(connnum, "【系统提示】{} 离开聊天室！".format(mydict[connnum]))
            myconnection.close()
            return

while True:
    connection, addr = server.accept()
    print "accept a new connect: {}:{}".format(connection.getsockname(), connection.fileno())
    try:
        buffer = connection.recv(1024).decode('utf8')
        if buffer == '1':
            connection.send(b'welcome to server!')
            mythread = threading.Thread(target=forthread, args=(connection, connection.fileno()))
            mythread.setDaemon(True)
            mythread.start()
        else:
            connection.send(b'please go out.')
            connection.close()
    except:
        pass
