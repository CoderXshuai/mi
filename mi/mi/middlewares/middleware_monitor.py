# -*- coding: utf-8 -*-
import redis
import time

Time = lambda: time.strftime('%Y-%m-%d %H:%M:%S')

class StatcollectorMiddleware(object):
    # 用于初始化,与实际服务无关
    r = redis.Redis(host="127.0.0.1", port="6379", db=0)
    timer = lambda: time.strftime('%Y-%m-%d %H:%M:%S')
    def __init__(self, settings):
        REDIS_HOST = settings.get('REDIS_HOST')
        REDIS_PORT = settings.get('REDIS_PORT')
        REDIS_DB = settings.get('MONITOR_DB')
        STATS_KEYS = settings.get('STATS_KEYS')
        self.r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
        self.stats_keys = STATS_KEYS

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_request(self, request, spider):
        self.formatStats(spider.crawler.stats.get_stats(), spider.name)

    def formatStats(self, stats, name):
        time = Time()
        for key in self.stats_keys:
            key_value = stats.get(key, None)
            if not key_value: key_value = 0
            value = {"value": [time, key_value]}
            self.r.rpush(key + "_" + name, value)
        time = Time()
        for key in self.stats_keys:
            sum = 0
            redis_keys = self.r.keys()
            for redis_key in redis_keys:
                if key in redis_key and key != redis_key:
                    one_part_of_value = self.r.lindex(redis_key, -1)
                    if one_part_of_value is not None:
                        sum = sum + eval(one_part_of_value)['value'][1]
            value = {"value": [time, sum]}
            self.r.rpush(key, value)