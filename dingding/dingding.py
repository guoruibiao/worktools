# coding: utf8

# @Author: 郭 璞
# @File: dingding.py
# @Time: 2017/9/2                                   
# @Contact: 1064319632@qq.com
# @blog: http://blog.csdn.net/marksinoberg
# @Description: 测试一下钉钉的机器人hook

import requests
import json
import time
import random
from bs4 import BeautifulSoup


class DDSender(object):
    """
    钉钉自定义聊天机器人，基于webhook.
    """

    def __init__(self, webhook):
        if webhook == "":
            print("有了webhook才能玩的，少侠！")
            exit(1)
        self.webhook = webhook
        # 没有请求头的话，无法认证以及控制data的编码格式。
        self.header = {
            "Content-Type": "application/json;charset=UTF-8",
        }

    def generateText(self, content, mobiles=[], isatall=False):
        data = {
            "msgtype": "text",
            "text": {
                "content": content
            },
            "at": {
                "atMobiles": [str(mobile) for mobile in mobiles]
            },
            "isAtAll": isatall
        }
        return json.dumps(data)

    def generateLink(self, title, content, picurl='', messageurl=''):
        data = {
            "msgtype": "link",
            "link": {
                "text": content,
                "title": title,
                "picUrl": picurl,
                "messageUrl": messageurl
            }
        }
        return json.dumps(data)

    def contentFormat(self, content):
        """
        目标格式如下：
          content: {
              title: "报警的title信息",
              error: error简要描述
              host: {
                  "ip": ip,
                  "summary": 错误的summary信息
              },
              authors: ['author1', 'author2', 'author3'],
              server: {
                  name: "server name",
                  link: "server's link for monitor"
              }
          }

        生成效果如下：
            错误：
            host: 192.168.1.93:3306
            summary: error sql
            主机：
            host216
            代码作者：
            everest
            SERVER-128
        """
        details = {}
        error = "\n#### **<font color='red' size='19'>" + content['error']+"</font>**\n\n"
        host = "#### 服务器简述：\n > Host:" + content['host']['ip'] +"\n" + "\n> summary:"+content['host']['summary'] +"\n\n---"
        authors = "\n\n#### <font color='green'>**代码作者: **</font>\n"
        authors += ("\n").join(["  - "+author for author in content['authors']]) + "\n\n"
        server = "---\n\n 查看监控→→→ [{}]({})\n".format(content['server']['name'], content['server']['link'])
        details['text'] = error + host+authors+server
        return details

    def generateMD(self, title="报警信息", details={}, mobiles=[], isatall=False):
        details = self.contentFormat(details)
        data = {
            "msgtype": "markdown",
            "markdown": {
                "title": title,
                "text": details['text']
            },
            "at": {
                "atMobiles": [str(mobile) for mobile in mobiles]
            },
            "isAtAll": isatall
        }
        return json.dumps(data)

    def send(self, data):
        response = requests.post(url=self.webhook, data=data, headers=self.header)
        if response.status_code == 200:
            result = json.loads(response.text)
            print("错误码：{}\n错误详情：{}".format(result['errcode'], result['errmsg']))


class Joker(object):
    """
    爬取笑话糗事，来测试文本信息。
    """

    def __init__(self):
        pass

    def getJoke(self):
        result = []
        headers = {
            'host': 'www.qiushibaike.com',
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
        }
        for index in range(3):
            url = 'http://www.qiushibaike.com/text/page/{}/'.format(index + 1)
            response = requests.get(url=url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            containers = soup.find_all("div", {"class": "article block untagged mb15 typs_hot"})
            for container in containers:
                content = container.find('a', {'class': 'contentHerf'}).find('div', {'class': 'content'}).find(
                    'span').get_text()
                content = content.lstrip('\n').rstrip('\n')
                result.append(content)
        return random.choice(result)


class News(object):
    """
    抓取新闻以及图片，来测试link消息类型。
    """

    def __init__(self):
        pass

    def getNews(self):
        result = []
        headers = {
            "Host": "geek.csdn.net",
            "Upgrade-Insecure-Requests": '1',
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
        }
        url = "http://geek.csdn.net"
        response = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        containers = soup.find_all('dl', {'class': "geek_list"})
        for container in containers:
            title = container.find("a", {'class': 'title'}).get_text()
            link = container.find('a', {"class": 'title'}).attrs['href']
            imgurl = container.find('img', {'class': 'avatar'}).attrs['src']
            result.append({'title': title, 'content': title, 'messageurl': link, 'imgurl': imgurl})

        return random.choice(result)


def main():
    # 苏，刘，我
    # dd = DDSender("https://oapi.dingtalk.com/robot/send?access_token=ac37261b8b7ae69bd17c69ed07088f7b41e07d0b39f26c25709d2442cc053d2828")
    # 唱吧实习5人行
    mobiles = ['phone number',]
    dd = DDSender(
        "https://oapi.dingtalk.com/robot/send?access_token=a6b51b474ebab06f39bc9c1349fea911cd80213d90bcbf4f14977dd85a56ed5b28")
    # markdown 测试，对于title的支持感觉不好
    details = {
        "error": "服务器又崩咯",
        "host": {
            "ip": "192.168.1.59",
            "summary": "最后一次测试了，⑧<(￣3￣)> "
        },
        "authors": ['张三', '李四', '王五', '赵六'],
        "server": {
            "name": "SERVER-59",
            "link": "http://example.com/"
        }

    }
    data = dd.generateMD(title="Σ( ° △ °|||)︴", details=details, mobiles=mobiles, isatall=True)
    news = News().getNews()
    joker = Joker().getJoke()
    # 文本测试
    data = dd.generateText(content=joker, mobiles=mobiles, isatall=False)
    dd.send(data=data)
    # print("暂时休眠7秒吧！")
    time.sleep(7)
    # link测试
    data = dd.generateLink(title=news['content'], content=news['content'], picurl=news['imgurl'],
                           messageurl=news['messageurl'])
    dd.send(data=data)


if __name__ == '__main__':
    main()
