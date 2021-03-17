# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from .settings import user_agent_list
import random
import requests
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class MeibangUserAgentMiddleware:
    def process_request(self, request, spider):
        ua = random.choice(user_agent_list)
        request.headers['User-Agent'] = ua

        return None


class MeibangProxyMiddle:
    def process_request(self, request, spider):
        proxy = requests.get("http://127.0.0.1:5010/get/").json().get("proxy")
        request.meta['proxy'] = f"http://{proxy}"

        return None

