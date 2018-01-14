#!/usr/bin python
# coding: utf8
# file: .py

import sys

reload(sys)
sys.setdefaultencoding('utf8')

import socket
import time
import threading
from colorcmd import *
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect(('localhost', 2222))
sock.send(b'1')
print(sock.recv(1024).decode())
nickName = raw_input('input your nickname: ')
nickname = Enhancer.highlight(nickName, Color.BACK_GREEN, Style.REVERSE+Style.UNDERLINE)
sock.send(nickName.encode())


def sendThreadFunc():
    global sock
    while True:
        try:
            myword = raw_input(">>>")
            myword = Enhancer.mix(myword, Color.FORE_GREEN, Style.BLINK)
            sock.send(myword.encode())
            # print(sock.recv(1024).decode())

        except Exception:
            print('Server is closed!')


def recvThreadFunc():
    global sock
    while True:
        try:
            otherword = sock.recv(1024)
            if otherword:
                print(otherword.decode())
            else:
                pass
        except Exception:
            print('Server is closed!')


th1 = threading.Thread(target=sendThreadFunc)
th2 = threading.Thread(target=recvThreadFunc)
threads = [th1, th2]

for t in threads:
    t.setDaemon(True)
    t.start()
t.join()
