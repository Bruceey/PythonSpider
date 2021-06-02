# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaItem(scrapy.Item):
    # 新房
    collection = 'xinFang'
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

    # 二手房
    erShouCollection = 'erShouFang'
    标题 = scrapy.Field()

    房屋户型 = scrapy.Field()
    所在楼层 = scrapy.Field()
    # 建筑面积
    户型结构 = scrapy.Field()
    套内面积 = scrapy.Field()
    # 建筑类型
    房屋朝向 = scrapy.Field()
    建筑结构 = scrapy.Field()
    装修情况 = scrapy.Field()
    梯户比例 = scrapy.Field()
    配备电梯 = scrapy.Field()

    挂牌时间 = scrapy.Field()
    交易权属 = scrapy.Field()
    上次交易 = scrapy.Field()
    房屋用途 = scrapy.Field()
    房屋年限 = scrapy.Field()
    产权所属 = scrapy.Field()
    抵押信息 = scrapy.Field()
    房本备件 = scrapy.Field()

    房源标签 = scrapy.Field()
    # 核心卖点 = scrapy.Field()
    # 小区介绍 = scrapy.Field()
    # 周边配套 = scrapy.Field()
    # 税费解析 = scrapy.Field()
    # 交通出行 = scrapy.Field()
    # 权属抵押 = scrapy.Field()
    房源特色 = scrapy.Field()

    # 租房
    zuShouCollection = 'zuFang'
    房源维护时间 = scrapy.Field()
    房源验真编号 = scrapy.Field()
    租赁方式 = scrapy.Field()
    房屋类型 = scrapy.Field()
    朝向楼层 = scrapy.Field()
    入住 = scrapy.Field()
    电梯 = scrapy.Field()
    车位 = scrapy.Field()
    用水 = scrapy.Field()
    用电 = scrapy.Field()
    燃气 = scrapy.Field()
    采暖 = scrapy.Field()
    租期 = scrapy.Field()
    看房 = scrapy.Field()
    配套设施 = scrapy.Field()
    付款方式 = scrapy.Field()
    租金 = scrapy.Field()
    押金 = scrapy.Field()
    服务费 = scrapy.Field()
    中介费 = scrapy.Field()


if __name__ == '__main__':
    item = LianjiaItem()
    item['联系方式'] = 'fasgseg'
    for k, v in item.items():
        print(k, v)