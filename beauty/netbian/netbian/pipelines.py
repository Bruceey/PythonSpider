# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import os

image_store = r"C:\Users\17634\Desktop\bian"
os.makedirs(image_store, exist_ok=True)

class NetbianPipeline:
    def process_item(self, item, spider):
        filename = item['filename']
        image_bytes = item['image_bytes']
        with open(os.path.join(image_store, filename), 'wb') as f:
            f.write(image_bytes)
        return item
