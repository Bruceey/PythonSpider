# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class ZhaopinPipeline:
    def __init__(self, mongo_url, mongo_db):
        self.mongo_url = mongo_url
        self.mongo_db = mongo_db

    def open_spider(self, spider):
        self.client = MongoClient(self.mongo_url)
        self.db = self.client[self.mongo_db]

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            crawler.settings.get('MONGO_URL'),
            crawler.settings.get('MONGO_DB')
        )

    def process_item(self, item, spider):
        if spider.name == 'boss':
            item = self.serialize(item)
            self.db['boss'].insert(item)
        return item


    def serialize(self, item):
        item = dict(item)
        for key, value in item.items():
            if isinstance(value, list):
                item[key] = ''.join(value)
        return item