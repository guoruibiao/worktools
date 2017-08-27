# coding: utf8

# @Author: 郭 璞
# @File: redishelper.py                                                                 
# @Time: 2017/8/27                                   
# @Contact: 1064319632@qq.com
# @blog: http://blog.csdn.net/marksinoberg
# @Description: 对redis的一个工具类。

import redis

class RedisHelper(object):

    def __init__(self, cfg={}):
        if cfg is None:
            print("配置内容为空的话，可是无法连接redis的哟！")
        else:
            self.r = redis.Redis(host=cfg['host'], port=int(cfg['port']), db=int(cfg['db'] if cfg['db'] else 0))

    def getTTL(self, key):
        return self.r.ttl(key)

    def getTTLs(self, keys):
        result = { key:self.getTTL(key=key) for key in keys}
        return result

    def getValue(self, key):
        return self.r.get(key)
    def setValue(self, key, value):
        self.r.set(key, value)

    def listLPush(self, key, items=[]):
        for item in items:
            self.r.lpush(key, item)
    def hashMSet(self, key, fields, values):
        if len(fields) == len(values):
            for index, field in enumerate(fields):
                self.r.hset(key, field,values[index])
    def hashSet(selfkey, field, value):
        self.r.hset(key, name, value)
    def hGetAll(self, key):
        return self.r.hget(key)

    def getKeys(self, pattern):
        if pattern:
            return self.r.keys(pattern=pattern)
        else:
            return self.r.keys()

    def getType(self, key):
        return self.r.type(key)

    def hashGet(self, key, field):
        return self.r.hget(key, field)
    def hashGetAll(self, key):
        return self.r.hgetall(key)

    def zRange(self, key, start, end, WITHSCORES):
        return self.r.zrange(key, start, end, WITHSCORES)
    def zRevRange(self, key, start, end, WITHSCORES):
        return self.r.zrevrange(key, start, end, WITHSCORES)

    def getLength(self, key):
        type = self.r.type(key)
        type = type.decode('utf8')
        if type == 'list':
            return self.r.llen(key)
        elif type == "string":
            return self.r.strlen(key)
        elif type == 'hash':
            return self.r.hlen(key)
        elif type == 'zset':
            return self.r.zcard(key)
        elif type == 'set':
            return self.r.scard(key)

    def isIn(self, key):
        type = self.r.type(key).decode('utf8')
        # 貌似list,zset不支持
        if type == "set":
            return self.r.sismember(key)
        elif type == 'hash':
            return self.r.hexists(key)

    def getValue(self,key, full=True, reverse=True, withscores=True):
        type = self.r.type(key).decode('utf8')
        if type == 'string':
            return self.r.get(key)
        elif type == 'list':
            if full:
                return self.r.lrange(key, 0, -1)
            else:
                return self.r.rpop()
        elif type == 'hash':
            return self.r.hgetall(key)
        elif type == 'zset':
            if full:
                if reverse:
                    if withscores:
                        return self.r.zrevrange(key, 0, -1, True)
                    else:
                        return self.r.zrevrange(key, 0, -1)
                else:
                    if withscores:
                        return self.r.zrange(key, 0, -1, True)
                    else:
                        return self.r.zrange(key, 0, -1)
            else:
                pass







