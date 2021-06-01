# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
import re

class LianjiaPipeline:
    """数据存到mongodb中"""

    def __init__(self, mongo_url, mongo_db):
        self.mongo_url = mongo_url
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_url=crawler.settings.get('MONGO_URL'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_url)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        data = dict(item)
        if spider.name == 'xinFang':
            data = self.process_xinfang_item(data)
            self.db[item.collection].insert(data)
        elif spider.name == 'erShouFang':
            data = self.process_ershou_item(data)
            self.db[item.erShouCollection].insert(data)
        return item

    def process_xinfang_item(self, item):
        """
        处理数据两端的空格
        :param item:
        :return:
        """
        for key, value in item.items():
            item[key] = self.serialize(value)
        return item

    def process_ershou_item(self, item):
        """
        处理数据两端的空格
        :param item:
        :return:
        """
        for key, value in item.items():
            if isinstance(value, list) and len(value) > 0:
                if key == '房源特色' or key == '房源标签':
                    # 处理房源特色部分
                    temp = ''
                    for s in value:
                        if re.match(r'[^0-9a-zA-Z]{4}', s):
                            temp += (s + ': ')
                        else:
                            temp += s
                    item[key] = temp
                else:
                    item[key] = ''.join(value)
            else:
                item[key] = self.serialize(value)
        return item

    @staticmethod
    def serialize(value):
        if value == '' or value is None:
            return ''
        else:
            return str(value).strip()

    def close_spider(self, spider):
        self.client.close()
