# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhaopinItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    名字 = scrapy.Field()
    招聘状态 = scrapy.Field()
    薪资 = scrapy.Field()
    要求 = scrapy.Field()
    标签 = scrapy.Field()
    职位描述 = scrapy.Field()
    工作地址 = scrapy.Field()
    公司信息 = scrapy.Field()
