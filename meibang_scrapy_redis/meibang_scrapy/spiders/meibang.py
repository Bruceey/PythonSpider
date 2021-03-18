import scrapy
from ..items import MeibangScrapyItem
import re
from scrapy_redis.spiders import RedisSpider



class MeibangSpider(RedisSpider):
    name = 'meibang'
    # download_timeout = 5
    allowed_domains = ['www.meibang88.com']

    # start_urls = ['http://www.meibang88.com/mote/']

    # 起始url所在redis中的key
    redis_key = "meibang:start_urls"

    def parse(self, response):
        lis = response.css('.hezi_t>ul>li')
        for li in lis:
            # 美女名字，后续用于命名文件夹
            beauty_name = li.css('li>p>a::text').get()
            # 该美女主页相对url
            beauty_homepage_url = li.css('li>p>a::attr(href)').get()
            beauty_homepage_url = response.urljoin(beauty_homepage_url)
            yield scrapy.Request(beauty_homepage_url, callback=self.parse_group, meta={'beauty_name': beauty_name})

    def parse_group(self, response):
        """获取美女主页每套写真url"""
        # 接收上方的beauty_name
        beauty_name = response.meta['beauty_name']
        lis = response.css('#list>li')
        for li in lis:
            group_url = li.css("li>p.biaoti>a::attr(href)").get()
            # 获取每套写真url
            group_url = response.urljoin(group_url)
            # 获取每套写真的title标题，用于下载图片命名的前缀
            title = li.css("li>p.biaoti>a::text").get().strip()
            # 去除命名的非法字符
            title = re.sub(r'[\\/:*?"<>|]', '', title)
            yield scrapy.Request(group_url, callback=self.parse_img_src, meta={'beauty_name': beauty_name, "title": title})

    def parse_img_src(self, response):
        """获取每张图片的src地址"""
        #拿到上方传递的beauty_name和title
        beauty_name = response.meta['beauty_name']
        title = response.meta['title']

        image_urls = response.css(".content>img::attr(src)").extract()
        item = MeibangScrapyItem(image_urls=image_urls, file_dir=beauty_name, filename_prefix=title)
        yield item

        # 获取下一页链接(如果该套图还有分页)
        next_elements = response.css("#pages>.a1")
        if next_elements and next_elements[-2].xpath('./text()').get() == "下一页":
            next_url = response.css("#pages>.a1::attr(href)")[-2].get()
            next_url = response.urljoin(next_url)
            yield scrapy.Request(next_url, callback=self.parse_img_src, meta={'beauty_name': beauty_name, "title": title})
