import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import ChinaItem


class ChinaSpider(CrawlSpider):
    name = 'china'
    allowed_domains = ['tech.china.com']
    start_urls = ['https://tech.china.com/articles/']

    rules = (
        Rule(LinkExtractor(allow=r'article/.*?\.html', restrict_css='.wntjItem'), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths='//a[contains(., "下一页")]')),
    )

    def parse_item(self, response):
        item = ChinaItem()
        item['title'] = response.xpath('//h1[@id="chan_newsTitle"]/text()').get()
        item['url'] = response.url
        item['text'] = ''.join(response.xpath('//div[@id="chan_newsDetail"]//text()').extract()).strip()
        item['datetime'] = response.css('.chan_newsInfo_source>.time::text').get()
        item['source'] = response.css('.chan_newsInfo_source>.source::text').re_first(r'来源：(.*)').strip()
        item['website'] = '中华网'
        yield item
