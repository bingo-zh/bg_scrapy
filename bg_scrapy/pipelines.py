# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting


from .util.MongoDBUtil import MongoDBUtil


class BgScrapyPipeline(object):
    config_obj = {
        'JdCatsItem': {
            'name': 'JdCatsItem',
            'count': 10,
            'data_list': []
        },
        'JdGoodsItem': {
            'name': 'JdGoodsItem',
            'count': 1000,
            'data_list': []
        },
        'LiepinItem': {
            'name': 'LiepinItem',
            'count': 1000,
            'data_list': []
        }
    }

    def __init__(self):
        self.mongo = MongoDBUtil()

    def process_item(self, item, spider):
        collection_name = item.__class__.__name__
        obj = self.config_obj[collection_name]
        name = obj['name']
        count = obj['count']
        data_list = obj['data_list']

        if len(data_list) == count:
            self.mongo.get_coll(name).insert_many(data_list)
            obj['data_list'] = []
        else:
            obj['data_list'].append(item)
        return item

    def close_spider(self, spider):
        for i in self.config_obj:
            obj = self.config_obj[i]
            self.mongo.get_coll(obj['name']).insert_many(obj['data_list'])
        self.mongo.close_client()
