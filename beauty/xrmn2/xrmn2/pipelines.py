# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import os

IMAGES_STORE = r"C:\Users\17634\Desktop\杨晨晨"
os.makedirs(IMAGES_STORE, exist_ok=True)


class Xrmn2Pipeline:
    def process_item(self, item, spider):
        title = item['title']
        image_serial = item['image_serial']
        image_bytes = item['image_bytes']
        dirname = os.path.join(IMAGES_STORE, title)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        file_path = os.path.join(dirname, f"{image_serial}.jpg")
        with open(file_path, 'wb') as f:
            f.write(image_bytes)