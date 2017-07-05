# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import scrapy
import json
import os

from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline


class MynewsPipeline(object):
    # 连接数据库
    # def __init__(self):
    #     print("###############################")
    #     connection = pymongo.connection(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
    #     #数据库
    #     db = connection[settings['MONGODB_DB']]
    #     # self.table = db[settings['MONGODB_TABLE']]
    #     self.connection=db[settings['MONGODB_CONNECTION']]
    #
    # def process_item(self, item, spider):
    #     print("###########process_item########")
    #     valid = True
    #     for data in item:
    #         if not data:
    #             valid = False
    #             raise DropItem('Missing{0}!'.format(data))
    #     if valid:
    #         self.connection.insert(dict(item))
    #     return item

    collection_content_name = 'news_content'
    db_name = 'my_news'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        MONGODB_URI = os.environ.get('MONGODB_URI')
        if not MONGODB_URI:
            print('================not mongo uri==============')
            return cls(
                mongo_uri=crawler.settings.get('MONGO_URI'),
                mongo_db=crawler.settings.get('MONGO_DATABASE', cls.db_name)
            )
        else:
            print('================has mongo uri==============')
            return cls(
                mongo_uri=crawler.settings.get(MONGODB_URI),
                mongo_db=crawler.settings.get('MONGO_DATABASE', cls.db_name)
            )


    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        # 有内容则插入数据库
        if item['content'] is not None:
            self.db[self.collection_content_name].insert_one(dict(item))
        return item


class MyImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item
