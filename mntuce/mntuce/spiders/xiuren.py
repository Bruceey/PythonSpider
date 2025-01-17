import scrapy
import re, os
from mntuce.items import MntuceItem
import logging
from scrapy.utils.log import _scrapy_root_handler


class XiurenSpider(scrapy.Spider):
    name = "xiuren"
    # allowed_domains = ["www.mntuce.com"]
    # 某个actress的主页，所有照片
    start_urls = [
        # "https://www.mntuce.com/tag/carol%e5%91%a8%e5%a6%8d%e5%b8%8cx", # Carol周妍希X
        # "https://www.mntuce.com/tag/%e7%8e%8b%e5%a9%89%e6%82%a0queen", # 王婉悠Queen
        # "https://www.mntuce.com/tag/%e5%bf%83%e5%a6%8d%e5%b0%8f%e5%85%ac%e4%b8%bb", # 心妍小公主
        # "https://www.mntuce.com/tag/%e9%87%91%e5%85%81%e7%8f%8d%e5%91%90", # 金允珍呐
        'https://www.mntuce.com/tag/%e5%b0%a4%e5%a6%ae%e4%b8%9degg', # 尤妮丝Egg
        ]

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super().from_crawler(crawler, *args, **kwargs)
        # 记录爬取的actress的album信息目录
        spider.record = 'record'
        os.makedirs(spider.record, exist_ok=True)
        # 设置配置LOG_FILE时同时输出终端和file
        filename = crawler.settings.get("LOG_FILE")
        if filename:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(fmt=crawler.settings.get("LOG_FORMAT"), datefmt=crawler.settings.get("LOG_DATEFORMAT"))
            handler.setFormatter(formatter)
            handler.setLevel(crawler.settings.get("LOG_LEVEL"))
            logging.root.addHandler(handler)

            # 生成另一个log，专门记录ERROR日志
            name, suffix = filename.rsplit('.', 1)
            fileHandler = logging.FileHandler(f'{name}_error.{suffix}', mode='w')
            fileHandler.setFormatter(formatter)
            fileHandler.setLevel('ERROR')
            logging.root.addHandler(fileHandler)
        return spider
    
    # def parse(self, response):
    #     return self.parse_album(response)

    def parse(self, response):
        """抓取actress的所有专辑"""
        # 1. 获取总体有多少本albums
        overall_info = response.meta.get('overall_info', None)
        if overall_info is None:
            overall_info = response.xpath('//h4//text()').extract()
            overall_info = '\t'.join(overall_info) + '\n'
            self.__setattr__('overall_info', overall_info)

        # 2. 提取albums
        albums = response.css('.item-thumbnail a::attr(href)').extract()
        # 获取album的名字
        a_eles = response.xpath('//h2[@class="item-heading"]/a')
        album_names = []
        for a in a_eles:
            album_name = a.xpath('.//text()').extract()
            album_name = ''.join(album_name)
            # 这里的album_name没有过滤特殊字符
            album_names.append(album_name)

        # 3. 获取美女actress
        actress = response.xpath('//h4//text()').get().strip()
        os.makedirs(f'./{self.record}/{actress}', exist_ok=True)
        # 判断spider是否有actress属性，并添加
        if getattr(self, "actress", None) is None:
            self.actress = actress
        # import rich
        # rich.print(os.getcwd())
        # 朝下一个解析函数输出
        ###### debug使用 ##################
        # album_names = album_names[:1]
        # albums = albums[:1]
        ###### debug使用 #################
        for album_name, album in zip(album_names, albums):
            # 写入当前album信息
            with open(f'./{self.record}/{actress}/{album_name}', 'w') as f:
                f.write(album)
            yield response.follow(album, callback=self.parse_album, meta={'album_name': album_name, 'actress': actress})

        #### 获取下一页 ########
        next_page = response.css('.next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, meta={'overall_info': overall_info})

    def parse_album(self, response):
        """抓取专辑，如某个专辑有多少照片，https://www.mntuce.com/16126/.html"""
        first = response.meta.get('first', True)
        actress = response.meta.get('actress', None)
        album_name = response.meta.get('album_name', None)
        if album_name is None:
            album_name = response.xpath('//h1/a//text()').extract()
            album_name = [s.strip() for s in album_name]
            album_name = ''.join(album_name)
        # 替换掉特殊字符
        album_name = re.sub(r'[\\/:*?"<>|]', "", album_name).strip()

        # if actress is None:
        #     actress = response.xpath('//a[@class="but ml6 radius"]/text()').extract()[-1].strip('# ')
        srcs = response.css('.article-content img::attr(src)').extract()
        yield MntuceItem(image_urls=srcs, actress=actress, album_name=album_name, referer=response.url)
        if first:
            next_pages = response.css('.text-center a::attr(href)').extract()
            for page in next_pages:
                yield response.follow(page, meta={'first': False, 'actress': actress, 'album_name': album_name}, callback=self.parse_album)
            

