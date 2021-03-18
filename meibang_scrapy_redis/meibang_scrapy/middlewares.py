# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from .settings import user_agent_list
import random
import requests
from requests.exceptions import Timeout
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class MeibangUserAgentMiddleware:
    """设置随机请求头"""
    def process_request(self, request, spider):
        ua = random.choice(user_agent_list)
        request.headers['User-Agent'] = ua
        return None


class MeibangProxyMiddle:
    """
        配置代理池，如果不需要代理池，可以在settings.py中关闭；
    """
    def process_request(self, request, spider):
        # 如上一次请求失败，retry_times将记录重试次数，
        # 反之请求成功retry_times为None，则继续使用本地ip
        if not request.meta.get('retry_times'):
            return None

        # 本地ip被封，请求代理池ip
        proxy = self.get_proxy()
        request.meta['proxy'] = f"http://{proxy}"
        # print(f"request对象是:\n{request.__dict__}")
        return None

    # def process_response(self, request, response, spider):
    #     if response.status < 200 or response.status >= 300:
    #         print('请求失败状态码：', response.status)
    #         return request
    #     return response

    @staticmethod
    def get_proxy():
        """获取代理池ip"""
        while True:
            proxy = requests.get("http://127.0.0.1:5010/get/").json().get('proxy')
            # 如果proxy不为空
            if proxy:
                break
        return proxy