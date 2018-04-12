# coding:utf8
import re
import os
import smtplib
import argparse
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


class Mailer(object):
    """
    邮件工具箱， 用于发送通用文本邮件以及各种附件形式的邮件。
    """
    def __init__(self, username="spidersmall@163.com", password="", host="smtp.163.com", port=25):
        if self._checkMailAddress(mailaddress=username) == False:
            raise Exception("发件人邮件地址有误，当前值：{}".format(username))
        self.username = str(username)
        # 初始化收件人列表
        self.receivers = []
        self._login(str(username), str(password), str(host), int(port))
        self.message = MIMEMultipart()
    
    def _login(self, username, password, host, port):
        self.client = smtplib.SMTP()
        self.client.connect(host, port)
        self.client.login(username, password)
    
    def _checkMailAddress(self, mailaddress=""):
        if mailaddress == "" or mailaddress is None:
            raise Exception("邮箱地址为空，当前值：{}".format(mailaddress))
        if len(mailaddress) < 6:
            raise Exception("邮箱[{}]长度太少了吧，确定没有输入错误吗？".format(mailaddress))
        regpattern = "^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$"
        if re.match(re.compile(regpattern), mailaddress) is not None:
            return True
        else:
            return False
        
    def addReceiver(self, receiver=""):
        if not self._checkMailAddress(mailaddress=receiver):
            raise Exception("收件人邮箱格式有误，当前值：{}".format(receiver))
        self.receivers.append(receiver)

    def _getContent(self, filename="", mode="r"):
        """
        这里mode最重要，需要自己指定读文件的模式，像xlsx，mp3这种二进制的，一定要用rb；普通文件用r模式即可。
        """
        content = ""
        mode = str(mode).lower()
        if os.path.exists(filename) == False:
            raise Exception("附件路径不存在，请确认后再发送吧~ \n当前值: {}".format(filename))
        if mode == "r":
            with open(filename, mode, encoding='utf8') as f:
                content = f.read()
                f.close()
        elif mode == "rb":
            with open(filename, mode) as f:
                content = f.read()
                f.close()
        else:
            raise Exception("暂不支持的读文件模式，当前值：{}".format(mode))
        return content

    def addAttchment(self, filename=""):
        content = self._getContent(filename=filename, mode='rb')
        attachment = MIMEApplication(content)
        attachment.add_header("Content-Disposition", "attachment", filename=filename)
        self.message.attach(attachment)
    
    def addMailBody(self, filename=""):
        content = self._getContent(filename=filename, mode='r')
        mailbody = MIMEText(content)
        self.message.attach(mailbody)
    
    def addMailContent(self, content=""):
        if content is None or content == "":
            raise Exception("一句话邮件正文不能为空哈~")
        mailcontent = MIMEText(content)
        self.message.attach(mailcontent)

    def send(self, subject="忘了写标题~"):
        self.message['Subject'] = subject
        self.message["From"] = self.username
        self.message['To'] = ",".join(self.receivers)
        try:
            self.client.sendmail(self.username, self.receivers, self.message.as_string())
            self.client.quit()
            print("主题为：[{}]的邮件发送成功~\n".format(subject))
        except Exception as e:
            print("出了点问题，具体信息为：{}".format(e))


def main():
    """
    使用命令行参数，免得密码泄露什么的。
    """
    parser = argparse.ArgumentParser(description="命令行邮件发送工具")
    parser.add_argument("-s", "--sender", help="邮件发送人邮件地址")
    parser.add_argument("-p", "--password", help="邮件发送人对应的密码")
    parser.add_argument("-H", "--host", help="邮件服务器主机")
    parser.add_argument("-P", "--port", help="邮件服务器端口，默认25")
    parser.add_argument("-r", "--receivers", nargs="+", help="收件人列表，注意不能少于一个，而且多个收件人要用空格隔开")
    parser.add_argument("-a", "--attachment", action="append", help="附件的全路径，注意windows和linux上会稍有不同~, 多个附件的时候需要重复指定此参数~")
    parser.add_argument("-t", "--text", help="邮件正文部分，相当于纯文本模式")
    parser.add_argument("-S", "--subject", help="邮件主题")
    args = parser.parse_args()
    if args is None:
        raise Exception("命令行参数有误~")
    sender = args.sender
    password = args.password
    host = args.host
    port = int(args.port)

    mailer = Mailer(username=sender, password=password, host=host, port=port)
    if args.text is not None:
        mailer.addMailContent(content=str(args.text))
    for receiver in args.receivers:
        mailer.addReceiver(receiver=receiver)
    for attach in args.attachment:
        mailer.addAttchment(filename=attach)
    if args.subject is not None:
        mailer.send(subject=str(args.subject))


if __name__ == "__main__":
    main()
    