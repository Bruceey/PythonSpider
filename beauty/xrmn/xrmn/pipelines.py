# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request


class XrmnPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        image_urls = item['image_urls']
        image_serials = item['image_serials']
        for i in range(len(image_serials)):
            request = Request(image_urls[i])
            request.serial = image_serials[i]
            yield request

    def file_path(self, request, response=None, info=None, *, item=None):
        title = item['title']
        author = item['author']
        # return f'{title}/{request.serial}.jpg'
        return f'{author}/{title}_{request.serial}.jpg'