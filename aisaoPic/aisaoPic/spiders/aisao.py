import scrapy
from scrapy_redis.spiders import RedisSpider
import re
from ..items import AisaopicItem


class AisaoSpider(RedisSpider):
    name = 'aisao'
    allowed_domains = ['www.f4mm.com']
    # start_urls = ['https://www.f4mm.com/beauty']

    base_page_url = 'https://www.f4mm.com/beauty/{page}'

    def parse(self, response):
        # 获取总页数
        total_page = response.xpath('//a[@class="page-link"]/text()').extract()[-2]
        for page in range(1, int(total_page) + 1):
            page_url = self.base_page_url.format(page=page)
            yield scrapy.Request(page_url, callback=self.parse_page)

    def parse_page(self, response):
        group_urls = response.css('.gallery>a::attr(href)').extract()
        for group_url in group_urls:
            yield scrapy.Request(group_url, callback=self.parse_group)

    def parse_group(self, response):
        filename = response.xpath('//h1/text()').get()
        filename_pri = re.sub(r'[/\\\"\'@]', '', filename)
        image_urls = response.css('div[data-fancybox="gallery"]>img::attr(data-src)').extract()
        yield AisaopicItem(filename_pri=filename_pri, image_urls=image_urls)
