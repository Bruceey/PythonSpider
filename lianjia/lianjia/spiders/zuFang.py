import scrapy
from ..items import LianjiaItem
from ..settings import URL_FILE
import csv
import math


class ZuFangSpider(scrapy.Spider):
    name = 'zuFang'
    allowed_domains = ['lianjia.com']
    # start_urls = ['https://www.lianjia.com/city/']

    def start_requests(self):
        with open(URL_FILE) as f:
            reader = csv.reader(f)
            for province, city, city_index_url in reader:
                city_index_url = city_index_url + 'zufang/'
                yield scrapy.Request(city_index_url, meta={'data': (province, city)})

    def parse(self, response):
        data = response.meta['data']
        curPage = response.meta.get('curPage', 1)
        totalPage = response.meta.get('totalPage', None)
        if totalPage is None:
            total_count = response.css('.content__title--hl::text').re_first('\S+')
            # 一页30条
            totalPage = math.ceil(int(total_count) / 30)

        hrefs = response.css('.content__list--item>a::attr(href)').extract()
        for href in hrefs:
            yield scrapy.Request(response.urljoin(href), callback=self.parse_fang_index, meta={'data': data})

        # 翻页
        next_page = curPage + 1
        if next_page <= totalPage:
            next_page_url = f'https://bj.lianjia.com/zufang/pg{next_page}/'
            yield scrapy.Request(next_page_url, callback=self.parse, meta={'data': data, 'curPage': next_page, 'totalPage': totalPage})

    def parse_fang_index(self, response):
        """
        抓取每个租房首页的具体信息
        :param response:
        :return:
        """
        item = LianjiaItem()
        province, city = response.meta['data']
        item['省份'] = province
        item['城市'] = city
        item['区域位置'] = response.xpath('//div[@class="bread__nav w1150 bread__nav--bottom"]//text()').re(r'[^\s>]+')[1:]
        item['标题'] = response.css('.content__title::text').get().strip()
        item['房源维护时间'] = response.css('.content__subtitle::text').get().strip()
        item['房源验真编号'] = response.css('.gov_title::text').re_first(r'\S+?.+\S')
        price = response.xpath('//div[@class="content__aside--title"]/span/text()').re_first('\S+')
        unit = response.xpath('//div[@class="content__aside--title"]/text()').re('\S+')
        item['单价'] = price + ''.join(unit)
        # TODO 联系方式js加密
        # phone_data = response.xpath('//div[@class="brokerInfoText"]/div[@class="phone"]//text()').re('\S+')
        # item['联系方式'] = ''.join(i.strip() for i in phone_data if '微信' not in i)
        # 基本属性
        label = response.xpath('//p[@class="content__aside--tags"]//text()').re('\S+')
        item['房源标签'] = ', '.join(label) if label else ''
        item['租赁方式'] = response.xpath('//ul[@class="content__aside__list"]/li[1]/text()').get()
        item['房屋类型'] = response.xpath('//ul[@class="content__aside__list"]/li[2]/text()').get()
        item['朝向楼层'] = response.xpath('//ul[@class="content__aside__list"]/li[3]/span[last()]/text()').get()
        item['入住'] = response.xpath('//div[@class="content__article__info"]//li[6]/text()').get()
        item['电梯'] = response.xpath('//div[@class="content__article__info"]//li[9]/text()').get()
        item['车位'] = response.xpath('//div[@class="content__article__info"]//li[11]/text()').get()
        item['用水'] = response.xpath('//div[@class="content__article__info"]//li[12]/text()').get()
        item['用电'] = response.xpath('//div[@class="content__article__info"]//li[14]/text()').get()
        item['燃气'] = response.xpath('//div[@class="content__article__info"]//li[15]/text()').get()
        item['采暖'] = response.xpath('//div[@class="content__article__info"]//li[17]/text()').get()
        item['租期'] = response.xpath('//div[@class="content__article__info"]//li[19]/text()').get()
        item['看房'] = response.xpath('//div[@class="content__article__info"]//li[22]/text()').get()
        facilities = response.xpath('//ul[@class="content__article__info2"]/li[@class="fl oneline  "]/text()').re('\S+')
        item['配套设施'] = ', '.join(facilities) if facilities else ''
        item['付款方式'], item['租金'], item['押金'], item['服务费'],  item['中介费'] = response.css('.table_row>li::text').extract()

        yield item


