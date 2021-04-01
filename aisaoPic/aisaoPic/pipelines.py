# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline


class AisaopicPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        filename_pri = ItemAdapter(item).get('filename_pri')
        filename_suf = '_'.join(request.url.split("/")[-3:])
        filename = filename_pri + filename_suf
        return filename
