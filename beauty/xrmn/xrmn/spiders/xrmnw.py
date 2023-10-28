import scrapy
# from xrmn.items import XrmnItem
from ..items import XrmnItem
#

class XrmnwSpider(scrapy.Spider):
    name = 'xrmnw'
    # allowed_domains = ['xrmn01.cc']
    # start_urls = ['https://www.xrmn01.cc/plus/search/index.asp?keyword=杨晨晨&p=2']
    # start_urls = ['https://www.xrmn02.cc/XiuRen/2023/202313494.html']
    # start_urls = ['https://www.xrmn02.cc/XiaoYu/2023/202313585.html']
    start_urls = ['https://www.xrmn02.cc/XiuRen/2023/202313611.html']

    # def parse(self, response, **kwargs):
    #     first_in = response.meta.get('first_in', True)
    #     if first_in:
    #         group_page_links = response.css('.page a::attr(href)').extract()
    #         # group_page_links = group_page_links[:2] if len(group_page_links) > 5 else group_page_links
    #         #####################
    #         for group_page in group_page_links:
    #             group_page = response.urljoin(group_page)
    #             yield scrapy.Request(group_page, meta={"first_in": False})
    #
    #     image_group_links = response.css('.sousuo a::attr(href)').extract()
    #     for group_link in image_group_links:
    #         group_link = response.urljoin(group_link)
    #         yield scrapy.Request(group_link, callback=self.parse_group_link)

    def parse(self, response, **kwargs):
        return self.parse_group_link(response)

    def parse_group_link(self, response):
        "https://www.xrmnw.cc/YouMi/2022/202211914.html"
        title = response.meta.get('title')
        # 首次title为空
        if title is None:
            title = response.css('h1::text').get()
            # 获取所有页面链接
            page_links = response.css('.page a::attr(href)').extract()
            # page_links = page_links[1: -1] #此处不需要过滤，scrapy会自动去掉重复请求链接
            for link in page_links:
                link = response.urljoin(link)
                yield scrapy.Request(link, callback=self.parse_group_link, meta={'title': title})

        image_urls = response.css('div.content_left p img::attr(src)').extract()
        # image_urls = [response.urljoin(url).replace('www.xrmnw.cc/uploadfile', "t.xrmnw.cc/Uploadfile") for url in image_urls]
        # https://www.xrmnw.xyz/uploadfile/202305/17/92165358253.jpg
        # https://xr.tp5.club/Uploadfile/202305/17/92165358253.jpg
        image_urls = [response.urljoin(url) for url in image_urls]
        # 获取当前页
        current_page = response.css('.current::text').get()
        current_page = int(current_page)
        image_serials = [(current_page - 1) * 3 + i + 1 for i in range(len(image_urls))]
        yield XrmnItem(image_urls=image_urls, image_serials=image_serials, title=title)

    @classmethod
    def check_groups_completely_downloaded(cls):
        pass
