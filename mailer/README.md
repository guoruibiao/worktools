外网工作环境下，下载文件上传文件都不是很方便，把数据给其他人就很难受，因此写了这样一个命令行工具，专门用来发邮件~


---

第一个不是很安全，尤其是在bash中输入密码等这种敏感信息。

更快捷的方式是使用alias

## 添加别名
```
vim ~/.bashrc
添加
alias sendmail='python /absolute file path/sendmail2.py'
激活环境变量
source ~/.bashrc
```
## 添加运行时配置文件
```
vim /etc/.mailerrc
```
添加下面的内容(按自己的实际情况而定)：
```
sender=xxxx@dddd.com
host=smtp.163.com
port=25
```


## 使用这个工具
然后就可以方便的查看了：

1. 查看帮助信息: `sendmail -h ` 或者 `sendmail --help`
```
root@ubuntu:~# sendmail --help
usage: sendmail2.py [-h] [-f FILE] [-r RECEIVERS [RECEIVERS ...]]
                    [-a ATTACHMENT] [-t TEXT] [-s SUBJECT]

命令行邮件发送工具

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  .mailerrc配置文件的位置
  -r RECEIVERS [RECEIVERS ...], --receivers RECEIVERS [RECEIVERS ...]
                        收件人列表，注意不能少于一个，而且多
                        个收件人要用空格隔开
  -a ATTACHMENT, --attachment ATTACHMENT
                        附件的全路径，注意windows和linux上会稍有
                        不同~,
                        多个附件的时候需要重复指定此参数~
  -t TEXT, --text TEXT  邮件正文部分，相当于纯文本模式
  -s SUBJECT, --subject SUBJECT
                        邮件主题
root@ubuntu:~# 

```

2. 发送邮件：

```
sendmail -r xxx@yyy.zzz -a  附件路径1 - 附件路径2 -t 邮件正文部分，可直接展示的文字 -s 邮件主题 
```

好了，差不多这样就好了。
