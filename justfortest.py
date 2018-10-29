# coding: utf8
import datetime
import requests
# 身份认证用，否则拿不到接口的数据
from utils.auth import *
import pymysql

def get_full_url():
    """
    到时候换成从配置文件中读取就行了,这里先拿'自助_shapi'里面的ApiDishController.getDish 接口
    """
    appkey = "ApiDishController.getDish"
    day = datetime.datetime.now()
    date = datetime.date(day.year, day.month, day.day)
    return "https://octo.sankuai.com/data/performance?appkey={0}&day={1}&env=prod&source=server".format(appkey, date)

def get_json(url=""):
    session = requests.session()
    auth = Auth(session)
    signdata = auth.get_sign_data()
    session.cookies['ssoid'] = signdata.get('SID')

    response = session.get(url=url)
    data = response.json()
    # 返回json格式的数据，对应内容为对应接口中的返回
    return data

def generate_sql(jsondata, appkey, group, date):
    """
    从json中拿到想要的数据，然后拼接成一条sql
    比如格式为：(appkey, group, count, value, self.date, datetime.datetime.now())
    """
    data = jsondata['data']
    count = data['count']
    topPercentile = all['topPercentile']
    # 比如我要拿到tp95的，我就这么组装
    value = topPercentile['upper95']
    return 'insert into t_b_api_tp95(appkey,api,groupname,tp95,date,addtime) values({0}, {1}, {2}, {3}, {4}, {5})'.\
        format("_shapi", "具体的api, 如getDish", "自助", value, date, datetime.datetime.now())




def insert_date(sql):
    """
    row 为 元组格式，形式为  (a, 'b', 12)等，按照表结构和字段类型即可
    """
    config = {
        'user': 'meishi_qa',
        'passwd': 'famEUMAkjAz6Y',
        'host': 'mysqldev56.vip.sankuai.com',
        'port': 5002,
        'db': 'test_meishi_perf',
        'use_unicode': True,
        'charset': 'utf8'
    }
    conn = pymysql.connect(config)
    cursor = conn.cursor()
    try:
        # 一次执行多条的有cursor.executemany(sql, data)
        cursor.execute(sql)
    except Exception as E:
        print(E)
    conn.commit()
    conn.close()

def select_sql(sql):
    """
    拿到存储到mysql中的自己的数据
    """
    config = {
        'user': 'meishi_qa',
        'passwd': 'famEUMAkjAz6Y',
        'host': 'mysqldev56.vip.sankuai.com',
        'port': 5002,
        'db': 'test_meishi_perf',
        'use_unicode': True,
        'charset': 'utf8'
    }
    conn = pymysql.connect(config)
    cursor = conn.cursor()
    try:
        # 一次执行多条的有cursor.executemany(sql, data)
        count = cursor.execute(sql)
        # 拿一条数据
        result = cursor.fetchone()
    except Exception as E:
        print(E)
    conn.commit()
    conn.close()
    return result



if __name__ == "__main__":
    # 第一步，拼装URL，可以参考他们写的从配置文件中获取一部分，然后自己拼接的形式
    full_url = get_full_url()
    # 第二步，拿数据之前必须先进行auth， 否则拿不到数据；可以参考上面的Auth的实现，具体就是对一个认证的URL区post对应的数据，成功会返回数据，
    #        拿到里面的SID，也就是SessionId，这样方便下次直接使用get的方式获取接口的数据
    jsondata = get_json(url=full_url)
    appkey = "_shapi"
    group = "自助"
    # 参数准备ing，拿到昨天的数据。所以date设置为昨天
    d = datetime.datetime.now()
    oneday = datetime.timedelta(days=1)
    date = d - oneday
    # 第三步，将JSON数据解析后，拼接成自己的SQL语句，插入到数据库中；考虑到代码运行的效率，可以使用多线程的形式，这里由于是演示，暂时不这么做，
    sql = genersql(jsondata, appkey, group, date)
    # 第四部，将拼接好的数据库中，具体思路就是：python链接mysql -> 拿到sql语句 -> 执行sql语句 -> commit，让改动在数据库内生效
    insert_date(sql)
    # 第五部，获取数据，直接使用具体的SQL去取数据就好了，具体也是需要：python链接mysql -> 拿到sql语句 -> 执行sql语句 -> 拿到数据
    sql = "select * from t_b_api_tp95 where appkey='_shapi' limit 1"
    row = select_sql(sql)
    print(row)
    #第六步， 拿到了数据后就可以用来展示了，用echarts或者转给其他的程序来展示都是可以的
    pass