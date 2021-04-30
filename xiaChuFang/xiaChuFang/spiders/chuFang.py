import scrapy
from ..items import XiachufangItem


class ChufangSpider(scrapy.Spider):
    name = 'chuFang'
    allowed_domains = ['xiachufang.com']
    start_urls = ['https://www.xiachufang.com/category/']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url,
                                 headers={
                                     'Referer': 'https://www.xiachufang.com/explore/menu/collect/',
                                     'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36'
                                 })

    def parse(self, response):
        divs = response.css('.cates-list')
        for div in divs:
            category1 = div.css('.cates-list-info h3::text').re_first('\S+')
            category2_url = div.css('.cates-list-all li a').re('href=\"(.*?)\".*?>(.*?)<')
            for i in range(0, len(category2_url), 2):
                url = response.urljoin(category2_url[i])
                category2 = category2_url[i+1]
                yield scrapy.Request(url, callback=self.parse_category2, meta={'category1': category1, 'category2': category2})

    def parse_category2(self, response):

        recipe_list = response.css('.normal-recipe-list>.list')[0]
        hrefs = recipe_list.css('.name a::attr(href)').extract()
        for href in hrefs:
            url = response.urljoin(href)
            yield scrapy.Request(url, callback=self.parse_detail, meta={'category1': response.meta['category1'], 'category2': response.meta['category2']})

        # 获取下一页
        next_page = response.xpath('//a[contains(., "下一页")]/@href').get()
        if next_page:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse_category2, meta={'category1': response.meta['category1'], 'category2': response.meta['category2']})

    def parse_detail(self, response):
        item = XiachufangItem()
        item['category1'] = response.meta['category1']
        item['category2'] = response.meta['category2']
        # 菜名
        item['name'] = response.css('h1::text').re_first('\S+')
        item['name_pic_url'] = response.css('.recipe-show .cover>img::attr(src)').get()
        item['score'] = response.css('.page-container .score span::text').get()
        item['cooked_number'] = response.css('.page-container .cooked span::text').get()
        item['author'] = response.css('.author a::text').re_first(r'\S+')
        # 配料
        dosing = response.css('.ings').re(r'<td class="name">\s*?(\S*?)\s*?</td>[\s.]*?<td class="unit">\s*?(\S*?)\s*?</td>')
        item['dosing'] = ','.join(dosing)
        # 做法
        steps = response.css('.steps li p::text').extract()
        item['steps'] = ''.join(steps)
        # 做法图片
        step_img_urls = response.css('.steps li img::attr(src)').extract()
        item['step_img_urls'] = ','.join(step_img_urls)
        tips = response.css('.tip::text').re(r'\S+')
        item['tips'] = ''.join(tips)
        yield item

