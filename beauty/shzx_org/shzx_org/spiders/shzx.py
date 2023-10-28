import scrapy
from ..items import ShzxOrgItem


class ShzxSpider(scrapy.Spider):
    name = "shzx"
    allowed_domains = ["shzx.org"]
    # start_urls = ["https://www.shzx.org/c/etagid24767-0.html"]  # 杨晨晨
    start_urls = ["https://www.shzx.org/c/etagid19963-0.html"]  # 尤妮丝

    # 某一个模特下所有套图
    # start_urls = ["https://www.shzx.org/c/etagid3035-0.html"]  # 王馨瑶
    def parse(self, response):
        group_links = response.xpath('//div[@class="b_txt"]//li/a[position()=last()]/@href').extract()
        # group_links = group_links[8:10] # 王馨瑶
        # group_links = group_links[5:10] # 杨晨晨
        group_links = group_links[5:]  # 尤妮丝
        for group_link in group_links:
            group_link = response.urljoin(group_link)
            yield scrapy.Request(group_link, callback=self.parse_img_src, meta={'first': True})

    def parse_img_src(self, response):
        # 是否第一次进来
        first = response.meta.get('first')
        # TODO windows下特殊字符问题处理，丢给moddlewares组件处理
        title = response.xpath('//h1/text()').get()
        image_urls = response.css('.main img::attr(src)').extract()
        current_page = response.css('.paging b::text').get()
        current_page = int(current_page.strip())
        image_serials = [(current_page - 1) * 2 + i for i in range(len(image_urls))]
        yield ShzxOrgItem(image_urls=image_urls, title=title, image_serials=image_serials)

        if first:
            # 所有页
            pages = response.css('.paging a::text').re_first(r'\d+')
            pages = int(pages)
            url = response.url
            base_url = url[:url.rindex('-') + 1] + '{}.html'
            for i in range(pages):
                url = base_url.format(i)
                yield scrapy.Request(url, callback=self.parse_img_src)
