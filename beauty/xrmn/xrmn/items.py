# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class XrmnItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # group_name = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    title = scrapy.Field()
    image_serials = scrapy.Field()
