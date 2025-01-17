import scrapy
import re, os
from mntuce.items import MntuceItem
import logging
from scrapy.utils.log import _scrapy_root_handler
from rich import print


class XiurenSpider(scrapy.Spider):
    name = "test"
    # allowed_domains = ["www.mntuce.com"]
    start_urls = ["https://www.mntuce.com/tag/carol%e5%91%a8%e5%a6%8d%e5%b8%8cx"] # 某个actress的主页，所有照片

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super().from_crawler(crawler, *args, **kwargs)
        # 记录爬取的actress的album信息目录
        spider.record = 'record'
        os.makedirs(spider.record, exist_ok=True)
        # 设置配置LOG_FILE时同时输出终端和file
        filename = crawler.settings.get("LOG_FILE")
        if filename:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(fmt=crawler.settings.get("LOG_FORMAT"), datefmt=crawler.settings.get("LOG_DATEFORMAT"))
            handler.setFormatter(formatter)
            handler.setLevel(crawler.settings.get("LOG_LEVEL"))
            logging.root.addHandler(handler)

            # 生成另一个log，专门记录ERROR日志
            name, suffix = filename.rsplit('.', 1)
            fileHandler = logging.FileHandler(f'{name}_error.{suffix}', mode='w')
            fileHandler.setFormatter(formatter)
            fileHandler.setLevel('ERROR')
            logging.root.addHandler(fileHandler)
        print(logging.root.handlers)
        logging.root.removeHandler(logging.root.handlers[0])
        print(logging.root.handlers)
        return spider
    
    # def parse(self, response):
    #     return self.parse_album(response)

    def parse(self, response):
        pass

