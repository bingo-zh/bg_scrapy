# -*- coding: utf-8 -*-
import redis

host = '47.74.51.196'
port = 6379
password = 'redis_123345'
db = 0


class RedisUtil(object):

    def __init__(self):
        super(RedisUtil, self).__init__()
        pool = redis.ConnectionPool(host=host, port=port, password=password, db=db)
        self.client = redis.Redis(connection_pool=pool)

    def get_client(self):
        return self.client

    def close_client(self):
        if self.client:
            self.client.close()
