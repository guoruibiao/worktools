#!/usr/bin python
# Author: 泰戈尔
# Date: 2019年07月27日
# Description: FAQ 生成器
# Usage:
#   source/catagory/xxx.md 
#   catagory 会作为左侧导航组
#   xxx.md 会作为组内具体FAQ
#   python faq-generator.py 就可以自动读取并生成index.html

import os
from collections import defaultdict

def get_group(sourcepath="./source/"):
    ret = defaultdict()
    for root, dirs, files in os.walk(sourcepath, topdown=True):
        # print(root, dirs, files)
        if root == sourcepath:
            for catagory in dirs:
                ret[catagory] = []
        else:
            key = root.lstrip(sourcepath)
            # print("key={}".format(key))
            ret[key] = ["{}/{}".format(root, filename) for filename in files]
    return ret

def parse_items(filename):
    """
    文件格式定死了，首行question，接着为具体问题内容；第三行而answer，接着后面全部为答案
    """
    ret = {"question":"", "answer":""}
    with open(filename, "r") as file:
        lines = file.readlines()
        file.close()
        try:
            ret["question"] = lines[1]
            ret["answer"] = "\n".join([item.strip("\n") for item in lines[3:]])
        except:
            pass
    return ret


def generate_faq_group(catagory, items):
    template = """<li class="cd-faq__title"><h2>{}</h2></li>""".format(catagory)
    itemsection = """
        <li class="cd-faq__item">
            <a class="cd-faq__trigger" href="#0"><span>{}</span></a>
            <div class="cd-faq__content">
                <div class="text-component">
                    <p>{}</p>
                </div>
            </div> <!-- cd-faq__content -->
        </li>
    """
    for item in items:
        # print(item)
        template += itemsection.format(item["question"], item["answer"])
    template = """
        <ul id="{}" class="cd-faq__group">
          {}
        </ul>
    """.format(catagory, template)
    return template


def generate_body(groups):
    body = ""
    for catagory, filenames in groups.items():
        items = []
        for filename in filenames:
            item = parse_items(filename)
            # print("item------", item)
            items.append(item)
        # print("items:", items)
        body += generate_faq_group(catagory, items)
    return body

def generate_catagories(groupnames=[]):
    template = """
    """
    isfirst = True if len(groupnames)>=1 else False
    for groupname in groupnames:
        if isfirst == True:
            template += """<li><a class="cd-faq__category cd-faq__category-selected truncate" href="#{}">{}</a></li>""".format(groupname, groupname)
            isfirst = False
        else:
            template += """<li><a class="cd-faq__category truncate" href="#{}">{}</a></li>""".format(groupname, groupname)
    template = """
    <ul class="cd-faq__categories">
        {}
    </ul>
    """.format(template)
    return template

def generate_html(groups):
    template = """
    <!doctype html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <script>document.getElementsByTagName("html")[0].className += " js";</script>
    <link rel="stylesheet" href="assets/css/style.css">
    <title>FAQ for mars</title>
    </head>
    <body>
    <header class="cd-header flex flex-column flex-center">
    <div class="text-component text-center">
        <h1>FAQ <small>for mars</small></h1>
        <p><a class="cd-article-link" href="#">火星内部FAQ汇总</a>  👈 </p>
    </div>
    </header>
    <section class="cd-faq js-cd-faq container max-width-md margin-top-lg margin-bottom-lg">
        <ul class="cd-faq__categories">
        {}
        </ul> <!-- cd-faq__categories -->

        <div class="cd-faq__items">
        {}
        </div>


	<a href="#0" class="cd-faq__close-panel text-replace">Close</a>
  
    <div class="cd-faq__overlay" aria-hidden="true"></div>
    </section> <!-- cd-faq -->
    <script src="assets/js/util.js"></script> <!-- util functions included in the CodyHouse framework -->
    <script src="assets/js/main.js"></script> 
    </body>
    </html>
    """
    catagories = generate_catagories(groups.keys())
    faqitems = generate_body(groups)
    return template.format(catagories, faqitems)

def main():
    sourcepath = "./source/"
    groups = get_group(sourcepath)
    html = generate_html(groups)
    with open("index.html", "w") as file:
        file.write(html)
        file.close
    print("生成完毕")

if __name__ == "__main__":
    main()