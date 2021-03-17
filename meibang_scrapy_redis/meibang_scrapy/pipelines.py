# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline


class MeibangImagePipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        file_dir = ItemAdapter(item).get('file_dir', '')
        filename = request.url.split('/')[-1]
        return f'{file_dir}/{filename}'
