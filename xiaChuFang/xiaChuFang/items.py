# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class XiachufangItem(scrapy.Item):
    # define the fields for your item here like:
    # 一级分类
    category1 = scrapy.Field()
    # 二级分类
    category2 = scrapy.Field()
    # 菜名
    name = scrapy.Field()
    # 菜名图片
    name_pic_url = scrapy.Field()
    # 评分
    score = scrapy.Field()
    # 做过的人数
    cooked_number = scrapy.Field()
    # 作者
    author = scrapy.Field()
    # 配料
    dosing = scrapy.Field()
    # 做法
    steps = scrapy.Field()
    # 做法图片
    step_img_urls = scrapy.Field()
    # 小贴士
    tips = scrapy.Field()
