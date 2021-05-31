# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaItem(scrapy.Item):
    collection = 'xinFang'
    # define the fields for your item here like:
    # name = scrapy.Field()
    省份 = scrapy.Field()
    城市 = scrapy.Field()
    区域位置 = scrapy.Field()
    小区 = scrapy.Field()
    别名 = scrapy.Field()
    在售状态 = scrapy.Field()
    物业类型 = scrapy.Field()
    单价 = scrapy.Field()
    价格附加信息 = scrapy.Field()
    最新开盘 = scrapy.Field()
    项目特色 = scrapy.Field()
    楼盘地址 = scrapy.Field()
    售楼处地址 = scrapy.Field()
    开发商 = scrapy.Field()
    建筑类型 = scrapy.Field()
    绿化率 = scrapy.Field()
    占地面积 = scrapy.Field()
    容积率 = scrapy.Field()
    建筑面积 = scrapy.Field()
    规划户数 = scrapy.Field()
    产权年限 = scrapy.Field()
    楼盘户型 = scrapy.Field()
    最近交房 = scrapy.Field()
    物业公司 = scrapy.Field()
    车位配比 = scrapy.Field()
    物业费 = scrapy.Field()
    供暖方式 = scrapy.Field()
    供水方式 = scrapy.Field()
    供电方式 = scrapy.Field()
    车位 = scrapy.Field()
    联系方式 = scrapy.Field()

if __name__ == '__main__':
    item = LianjiaItem()
    item['联系方式'] = 'fasgseg'
    for k, v in item.items():
        print(k, v)