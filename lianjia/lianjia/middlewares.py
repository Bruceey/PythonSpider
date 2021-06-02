# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
import time
import random
from twisted.internet.error import DNSLookupError
from scrapy.exceptions import IgnoreRequest
from fake_useragent import UserAgent
from .spiders.xinFang import XinFangSpider
from scrapy.http import TextResponse

ua = UserAgent()

class LianjiaSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class HeaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        if request.url.startswith('https://ex.lianjia.com/sdk/recommend/html/100011051'):
            request.headers['ketracespiddtid'] = self.get_ketracespiddtid()
        request.headers['User-Agent'] = ua.random
        return None

    @staticmethod
    def get_ketracespiddtid():
        e = str(hex(int(time.time())))[2:]
        t = str(hex(int(16777216 * random.random())))[2:]
        n = str(hex(int(65536 * random.random())))[2:]
        r = str(hex(int(16777216 * random.random())))[2:]
        s = "00000000"[:8 - len(e)] + e + "000000"[:6 - len(t)] + t + "0000"[:4 - len(n)] + n + "000000"[:6 - len(r)] + r
        ketracespiddtid = 'cq.fang.lianjia.com-' + s
        return ketracespiddtid

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # 没有新房时日志记录
        province, city = request.meta['data']
        if isinstance(exception, DNSLookupError) and isinstance(spider, XinFangSpider) and '/loupan' in request.url:
            spider.logger.error(f'{province}-{city} 没有新房。。。')
            raise IgnoreRequest()
            # return TextResponse(url=request.url, body='没有新房'.encode())
            # 没有二手房时日志记录
        elif isinstance(exception, DNSLookupError) and spider.name == 'erShouFang' and '/ershoufang' in request.url:
            spider.logger.error(f'{province}-{city} 没有二手房。。。')
            raise IgnoreRequest()
        elif isinstance(exception, DNSLookupError) and spider.name == 'zuFang' and '/zufang' in request.url:
            spider.logger.error(f'{province}-{city} 没有租房信息。。。')
            raise IgnoreRequest()

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

