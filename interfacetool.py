#!/usr/bin python
# coding: utf8
# Vim Runtime: /usr/share/vim/vim74
# File Name: exectools.py
# Author:  郭璞 
# Create Time: Sat 26 Aug 2017 09:18:46 PM CST
# Blog: http://blog.csdn.net/marksinoberg

import subprocess
import prettytable
from prettytable import PrettyTable as PT
import sys
from colorama import init, Fore, Back

#cmd = "wget http://fanyi.badu.com/v2transapi?query=hello | python -m json.tool"

cmd = "php {} | python -m json.tool".format(sys.argv[1])

p = subprocess.Popen(["php test.php | python -m json.tool", "python -m json.tool"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

result = ""
while True:
	data = p.stdout.readline()
	if data == b'':
		break
	else:
	    result += data.decode('ascii').encode('utf8').decode('utf8')

table = PT(["文件名称", "执行结果"])
init(autoreset=True)
filename = Fore.YELLOW + sys.argv[1]+''
table.add_row([filename, Fore.GREEN+result])
table.align='l'
print table

