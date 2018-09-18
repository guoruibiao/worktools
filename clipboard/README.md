对VPS环境等机器，没有窗口支持，所以xclip， xsel等会失效，报`Error: Can't open display: (null) when using Xclip`, 
  而在服务器环境上将命令暂时保留其实还蛮有用的，于是做了一个类似的假的操作系统剪切板的小脚本。
  

---

使用步骤：

1. 更改两个shell脚本（mycopy.sh 和 mypaste.sh）里面的路径，也就是clipboard.py所在的路径。


2. 在`~/.bashrc`中添加别名：
```
alias pbcopy='bash /xxxxx/mycopy.sh'
alias pbpaste='bash /xxxxx/mypaste.sh'
```

3. 让配置生效
```
source ~/.bashrc
```

4. 然后就可以愉快的使用这个假的命令工具了, 如：
```
root@ktv322:/tmp# cat anchordispatch-padding.log
[2018-09-11 20:00:07] 这里是日志信息
[2018-09-12 20:00:10] 这里是日志信息
[2018-09-13 20:00:09] 这里是日志信息
[2018-09-14 20:00:07] 这里是日志信息
[2018-09-15 20:00:08] 这里是日志信息
[2018-09-16 20:00:07] 这里是日志信息
[2018-09-17 20:00:08] 这里是日志信息
root@ktv322:/tmp#
root@ktv322:/tmp# cat anchordispatch-padding.log | awk '{print $1}' | cut -d'[' -f2
2018-09-11
2018-09-12
2018-09-13
2018-09-14
2018-09-15
2018-09-16
2018-09-17
root@ktv322:/tmp#
root@ktv322:/tmp# cat anchordispatch-padding.log | awk '{print $1}' | cut -d'[' -f2 | pbcopy
root@ktv322:/tmp# pbpaste
2018-09-11
2018-09-12
2018-09-13
2018-09-14
2018-09-15
2018-09-16
2018-09-17
root@ktv322:/tmp# cat /tmp/clip.txt
2018-09-11
2018-09-12
2018-09-13
2018-09-14
2018-09-15
2018-09-16
2018-09-17
root@ktv322:/tmp#
```

enjoy it.
