import scrapy
from ..items import LianjiaItem
from ..settings import URL_FILE
import csv
import math
import re


class erShouFangSpider(scrapy.Spider):
    name = 'erShouFang'
    allowed_domains = ['lianjia.com']
    # start_urls = ['https://www.lianjia.com/city/']

    def start_requests(self):
        with open(URL_FILE) as f:
            reader = csv.reader(f)
            for province, city, city_index_url in reader:
                if city == '北京':
                    index = city_index_url.find('.')
                    city_index_url = city_index_url + 'ershoufang/'
                    yield scrapy.Request(city_index_url, meta={'data': (province, city)})

    def parse(self, response):
        data = response.meta['data']
        curPage = response.meta.get('curPage', 1)
        totalPage = response.meta.get('totalPage', None)
        if totalPage is None:
            total_count = response.css('.total.fl span::text').re_first('\S+')
            # 一页30条
            totalPage = math.ceil(int(total_count) / 30)

        hrefs = response.css('.info .title>a::attr(href)').extract()
        for href in hrefs:
            yield scrapy.Request(response.urljoin(href), callback=self.parse_fang_index, meta={'data': data})

        # 翻页
        next_page = curPage + 1
        if next_page <= totalPage:
            next_page_url = f'https://bj.lianjia.com/ershoufang/pg{next_page}/'
            yield scrapy.Request(next_page_url, callback=self.parse, meta={'data': data, 'curPage': next_page, 'totalPage': totalPage})

    def parse_fang_index(self, response):
        """
        抓取每个房子的首页具体信息
        :param response:
        :return:
        """
        item = LianjiaItem()
        province, city = response.meta['data']
        item['省份'] = province
        item['城市'] = city
        item['区域位置'] = response.xpath('//div[@class="fl l-txt"]/a[3]/text()').get()
        temp1 = response.xpath('//div[@class="fl l-txt"]/a[4]/text()').get()
        temp2 = response.xpath('//div[@class="fl l-txt"]/a[5]/text()').get()
        item['小区'] = temp1 + '-' + temp2
        item['标题'] = response.css('h1::text').get()
        price = response.xpath('//div[@class="price "]//text()').re('.+')
        item['单价'] = ', '.join(i.strip() for i in price if '首付' not in i)
        phone_data = response.xpath('//div[@class="brokerInfoText"]/div[@class="phone"]//text()').re('\S+')
        item['联系方式'] = ''.join(i.strip() for i in phone_data if '微信' not in i)
        # 基本属性
        item['房屋户型'] = response.xpath('//div[@class="base"]//li[1]/text()').get()
        item['所在楼层'] = response.xpath('//div[@class="base"]//li[2]/text()').get()
        item['建筑面积'] = response.xpath('//div[@class="base"]//li[3]/text()').get()
        item['户型结构'] = response.xpath('//div[@class="base"]//li[4]/text()').get()
        item['套内面积'] = response.xpath('//div[@class="base"]//li[5]/text()').get()
        item['建筑类型'] = response.xpath('//div[@class="base"]//li[6]/text()').get()
        item['房屋朝向'] = response.xpath('//div[@class="base"]//li[7]/text()').get()
        item['建筑结构'] = response.xpath('//div[@class="base"]//li[8]/text()').get()
        item['装修情况'] = response.xpath('//div[@class="base"]//li[9]/text()').get()
        item['梯户比例'] = response.xpath('//div[@class="base"]//li[10]/text()').get()
        item['供暖方式'] = response.xpath('//div[@class="base"]//li[11]/text()').get()
        item['配备电梯'] = response.xpath('//div[@class="base"]//li[12]/text()').get()
        # 交易属性
        item['挂牌时间'] = response.xpath('//div[@class="transaction"]//li[1]/span[last()]/text()').get()
        item['交易权属'] = response.xpath('//div[@class="transaction"]//li[2]/span[last()]/text()').get()
        item['上次交易'] = response.xpath('//div[@class="transaction"]//li[3]/span[last()]/text()').get()
        item['房屋用途'] = response.xpath('//div[@class="transaction"]//li[4]/span[last()]/text()').get()
        item['房屋年限'] = response.xpath('//div[@class="transaction"]//li[5]/span[last()]/text()').get()
        item['产权所属'] = response.xpath('//div[@class="transaction"]//li[6]/span[last()]/text()').get()
        item['抵押信息'] = response.xpath('//div[@class="transaction"]//li[7]/span[last()]/text()').get()
        item['房本备件'] = response.xpath('//div[@class="transaction"]//li[8]/span[last()]/text()').get()

        # 房源特色
        item['房源标签'] = response.xpath('//div[@class="tags clear"]//text()').re('\S+')
        item['房源特色'] = response.xpath('//div[@class="baseattribute clear"]//text()').re('\S+')
        yield item


