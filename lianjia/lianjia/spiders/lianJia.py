import scrapy
from ..items import LianjiaItem
from ..settings import URL_FILE
import csv
import math
from urllib.parse import urlencode


class XinFangSpider(scrapy.Spider):
    name = 'xinFang'
    allowed_domains = ['lianjia.com']
    # start_urls = ['https://www.lianjia.com/city/']
    suffix = 'loupan/'

    def start_requests(self):
        with open(URL_FILE) as f:
            reader = csv.reader(f)
            for province, city, city_index_url in reader:
                if city == '北京':
                    index = city_index_url.find('.')
                    city_index_url = city_index_url[:index] + '.fang.' + city_index_url[index + 1:] + self.suffix
                    yield scrapy.Request(city_index_url, meta={'data': (province, city)})

    def parse(self, response):
        # text = getattr(response, 'text', None)
        # if '没有新房' in text:
        #     return
        data = response.meta['data']
        curPage = response.meta.get('curPage', 1)
        totalPage = response.meta.get('totalPage', None)
        if totalPage is None:
            total_count = response.css('.page-box::attr(data-total-count)').get()
            # 一页10条
            totalPage = math.ceil(int(total_count) / 10)

        hrefs = response.css('.resblock-name>a::attr(href)').extract()
        for href in hrefs:
            yield scrapy.Request(response.urljoin(href), callback=self.parse_fang_index, meta={'data': data})

        # 翻页
        next_page = curPage + 1
        if next_page <= totalPage:
            next_page_url = f'https://bj.fang.lianjia.com/loupan/pg{next_page}/'
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
        item['区域位置'], item['小区'] = response.xpath('//div[@class="breadcrumbs"]/a[position()>last()-2]/text()').extract()
        item['别名'] = response.css('.other-name::text').get()
        item['在售状态'] = response.css('.sell-type-tag::text').get()
        item['物业类型'] = response.css('.house-type-tag::text').get()
        price = response.css(
            'div.resblock-info.animation.qr-fixed > div > div.top-info > div.price>span::text').extract()
        item['单价'] = ', '.join(price)
        item['价格附加信息'] = response.css('.update-time::text').get()
        item['最新开盘'] = response.css('.open-date>span.content::text').get()
        yield scrapy.Request(response.urljoin('xiangqing'), callback=self.parse_fang_detail, meta={'item': item})

    def parse_fang_detail(self, response):
        item = response.meta['item']
        # 继续抓取其他信息

        uls = response.css('.x-box')

        # 基本信息
        item['项目特色'] = uls[0].xpath('./li[3]/span[last()]/text()').re_first(r'.+')
        item['楼盘地址'] = uls[0].xpath('./li[5]/span[last()]/text()').re_first(r'.+')
        item['售楼处地址'] = uls[0].xpath('./li[6]/span[last()]/text()').re_first(r'.+')
        item['开发商'] = uls[0].xpath('./li[7]/span[last()]/text()').re_first(r'.+')

        # 规划信息
        item['建筑类型'] = uls[1].xpath('./li[1]/span[last()]/text()').re_first(r'.+')
        item['绿化率'] = uls[1].xpath('./li[2]/span[last()]/text()').re_first(r'.+')
        item['占地面积'] = uls[1].xpath('./li[3]/span[last()]/text()').re_first(r'.+')
        item['容积率'] = uls[1].xpath('./li[4]/span[last()]/text()').re_first(r'.+')
        item['建筑面积'] = uls[1].xpath('./li[5]/span[last()]/text()').re_first(r'.+')
        item['规划户数'] = uls[1].xpath('./li[7]/span[last()]/text()').re_first(r'.+')
        item['产权年限'] = uls[1].xpath('./li[8]/span[last()]/text()').re_first(r'.+')
        temp = uls[1].xpath('./li[9]/span[last()]/a/text()').re(r'.+')
        item['楼盘户型'] = ', '.join(temp) if temp else ''
        item['最近交房'] = uls[1].xpath('./li[10]/span[last()]/text()').re_first(r'.+')

        # 配套信息
        item['物业公司'] = uls[2].xpath('./li[1]/span[last()]/text()').re_first(r'.+')
        item['车位配比'] = uls[2].xpath('./li[2]/span[last()]/text()').re_first(r'.+')
        item['物业费'] = uls[2].xpath('./li[3]/span[last()]/text()').re_first(r'.+')
        item['供暖方式'] = uls[2].xpath('./li[4]/span[last()]/text()').re_first(r'.+')
        item['供水方式'] = uls[2].xpath('./li[5]/span[last()]/text()').re_first(r'.+')
        item['供电方式'] = uls[2].xpath('./li[6]/span[last()]/text()').re_first(r'.+')
        item['车位'] = uls[2].xpath('./li[7]/span[last()]/text()').re_first(r'.+')

        # "楼盘纪事" 和 "售卖资格" 是两个表，此处不抓取

        # TODO 周边规划信息估计百度地图加密

        # 抓取联系电话
        # TODO 联系方式js加密获取
        __city__id = response.selector.re_first('__city__id.*?(\d+)')
        __project__name = response.selector.re_first('__project__name.*?([a-zA-Z]+)')
        params = {
            'hdicCityId': __city__id,
            'id': "100011051",
            'mediumId': '100000032',
            'projectName': __project__name,
            'projectType': '',
            'elementId': "tab-400",
            'required400': 'true',
            'parentSceneId': ''
        }
        phone_url = 'https://ex.lianjia.com/sdk/recommend/html/100011051?' + urlencode(params)
        yield scrapy.Request(phone_url, callback=self.parse_phone, meta={'item': item})

    def parse_phone(self, response):
        item = response.meta['item']
        json_data = response.json()
        item['联系方式'] = json_data['data']['agentList'][0]['phone400']
        # TODO 处理数据两端的空格
        item = self.process_item(item)
        yield item


    def process_item(self, item):
        """
        处理数据两端的空格
        :param item:
        :return:
        """
        def serialize(value):
            if value == '' or value is None:
                return ''
            else:
                return str(value).strip()

        for key, value in item.items():
            item[key] = serialize(value)
        return item
