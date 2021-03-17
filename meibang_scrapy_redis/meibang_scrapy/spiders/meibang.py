import scrapy
from ..items import MeibangScrapyItem
import re
from scrapy_redis.spiders import RedisSpider



class MeibangSpider(RedisSpider):
    name = 'meibang'
    allowed_domains = ['www.meibang88.com']

    # start_urls = ['http://www.meibang88.com/t/787/']

    def parse(self, response):
        lis = response.css('#list>li')
        for li in lis:
            group_url = li.css("li>p.biaoti>a::attr(href)").get()
            group_url = response.urljoin(group_url)
            title = li.css("li>p.biaoti>a::text").get().strip()
            title = re.sub(r'[\\/:*?"<>|]', '', title)
            yield scrapy.Request(group_url, callback=self.parse_img_src, meta={"title": title})

    def parse_img_src(self, response):
        image_urls = response.css(".content>img::attr(src)").extract()
        title = response.meta['title']
        item = MeibangScrapyItem(image_urls=image_urls, file_dir=title)
        yield item

        # 获取下一页链接
        next_elements = response.css("#pages>.a1")
        if next_elements and next_elements[-2].xpath('./text()').get() == "下一页":
            next_url = response.css("#pages>.a1::attr(href)")[-2].get()
            next_url = response.urljoin(next_url)
            yield scrapy.Request(next_url, callback=self.parse_img_src, meta={"title": title})
