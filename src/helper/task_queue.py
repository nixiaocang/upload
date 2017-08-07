#!/usr/bin/env python
# encoding:utf-8

import time
from json import dumps, loads

from redis import StrictRedis

from util.config import Configuration
from util.logger import task_logger

logger = task_logger()


class TaskQueue():
    KST_TYPE = 'kst'

    def __init__(self):
        conf = Configuration()
        host = conf.get("redis", "host")
        port = int(conf.get("redis", "port"))
        self.redis_key = "KST:QUEUE:%s" % conf.get("global", "subpub_prefix")
        try:
            self.handler = StrictRedis(host, port, retry_on_timeout=True, socket_timeout=300,
                                       socket_connect_timeout=300)
        except:
            self.handler = StrictRedis(host, port)

    def push(self, job, type):
        topic = "%s:%s" % (self.redis_key, type)

        if isinstance(job, (str, unicode)):
            job = [job]
        logger.info('push task : %s ===> %s' % (topic, dumps(job)))
        return self.handler.rpush(topic, dumps(job))

    def hset(self, field, job, type):
        topic = "%s:%s" % (self.redis_key, type)
        if isinstance(job, (str, unicode)):
            job = [job]
        return self.handler.hset(topic, field, dumps(job))

    def hdel(self, field, type):
        topic = "%s:%s" % (self.redis_key, type)
        return self.handler.hdel(topic, field)

    def pop(self, type):
        topic = "%s:%s" % (self.redis_key, type)
        while True:
            if self.size(topic) == 0:
                time.sleep(1)
                continue
            res = self.handler.lpop(topic)
            logger.info('pop task : %s ===> %s' % (topic, res))
            if res:
                yield loads(res)

    def size(self, topic):
        return self.handler.llen(topic)

    def get(self, key):
        topic = "%s:%s" % (self.redis_key, key)
        return self.handler.get(topic)

    def set(self, key, value, expire=3600):
        topic = "%s:%s" % (self.redis_key, key)
        self.handler.set(topic, value, ex=expire)


if __name__ == '__main__':
    TaskQueue()
