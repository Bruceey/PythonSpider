# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import os
import json


class ScrapyuniversalPipeline:
    def __init__(self, dir):
        self.dir = dir
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls(crawler.settings.get('FILE_STORE'))
        return s

    def process_item(self, item, spider):
        filename = item.get('url').split('/')[-1]
        filename = filename.replace('.html', '.json')
        filepath = os.path.join(self.dir, filename)
        with open(filepath, "w") as f:
            json.dump(dict(item), f, ensure_ascii=False)
        return item


if __name__ == '__main__':
    print(os.path.realpath(__file__))
