import scrapy
from ..items import NetbianItem


class BianSpider(scrapy.Spider):
    name = 'bian'
    allowed_domains = ['netbian.com']
    start_urls = ['http://www.netbian.com/meinv/']
    # start_urls = ['http://www.netbian.com/meinv/index_5.htm']

    def parse(self, response):
        """方法一：不断从当前页递进式获取下一页"""
        image_urls = response.css('.list li a::attr(href)').extract()
        for url in image_urls:
            if not url.startswith('http:'):
                url = response.urljoin(url)
                yield scrapy.Request(url, callback=self.parse_image_url)

        next_page = response.xpath('//div[@class="page"]//a[contains(.,"下一页")]/@href').get()
        if next_page:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page)

    # def parse(self, response):
    #     """方法二：从首页构建所有页面链接"""
    #     first_in = response.meta.get("first_in", True)
    #     if first_in:
    #         # 抓取其他页
    #         # total_page = response.css('.page a::attr(href)').re(r'index_(\d+)')[-2]
    #         total_page = response.css('.page a::text').extract()[-2]
    #         total_page = int(total_page)
    #         for i in range(5, total_page + 1 - 60):
    #             url = f"http://www.netbian.com/meinv/index_{i}.htm"
    #             yield scrapy.Request(url, callback=self.parse, meta={'first_in': False})

        image_urls = response.css('.list li a::attr(href)').extract()
        for url in image_urls:
            if not url.startswith('http:'):
                url = response.urljoin(url)
                yield scrapy.Request(url, callback=self.parse_image_url)


    def parse_image_url(self, response):
        image_src = response.css('.pic img::attr(src)').get()
        yield scrapy.Request(image_src, callback=self.parse_image_content)

    def parse_image_content(self, response):
        filename = response.url.split('/')[-1]
        image_bytes = response.body
        yield NetbianItem(filename=filename, image_bytes=image_bytes)
