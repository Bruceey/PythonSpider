import scrapy
from ..items import ZhaopinItem


class BossSpider(scrapy.Spider):
    name = 'boss'
    allowed_domains = ['zhipin.com']
    start_urls = ['https://www.zhipin.com/c101210100/?query=%E7%88%AC%E8%99%AB&page=1&ka=page-1']

    def parse(self, response):
        links = response.css('.job-name>a::attr(href)').extract()
        for link in links:
            link = response.urljoin(link)
            yield scrapy.Request(url=link, callback=self.parse_job)

        # 获取下一页
        next_page = response.xpath('//div[@class="page"]/a[@class="next"]/@href').get()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def parse_job(self, response):
        item = ZhaopinItem()
        item['名字'] = response.css('h1::text').get()
        item['招聘状态'] = response.css('.job-status>span::text').get()
        item['薪资'] = response.css('.salary::text').get()
        item['要求'] = response.xpath('//div[@class="job-primary detail-box"]/div[@class="info-primary"]/p[1]//text()').re('\S+')
        item['要求'] = ', '.join(item['要求'])
        item['标签'] = response.css('.job-primary .tag-all>span::text').extract()
        item['标签'] = ', '.join(item['标签'])
        item['职位描述'] = response.xpath('//div[@class="text"]//text()').re(r'\S+')
        item['工作地址'] = response.css('.location-address::text').get()
        item['公司信息'] = response.xpath('//div[@class="sider-company"]//text()').re(r'\S+')
        yield item
