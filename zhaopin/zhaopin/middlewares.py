# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
from scrapy.http.response.html import HtmlResponse
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from PIL import Image
import base64
import json
import requests
import time


class ZhaopinDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    def __init__(self):
        options = webdriver.ChromeOptions()
        # 处理证书错误
        options.add_argument('--ignore-certificate-errors')
        # 修改windows.navigator.webdriver，防机器人识别机制，selenium自动登陆判别机制
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_argument("--disable-blink-features=AutomationControlled")
        self.browser = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.browser, 10)

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        if spider.name == 'boss':
            self.browser.get(request.url)
            time.sleep(1)
            html = self.browser.page_source
            # 点击关掉登录提示框
            if '立即登录，享受优质服务' in html:
                self.browser.find_element_by_css_selector('.closeIcon').click()
                print("出现登录提示框，正在关闭...")
                time.sleep(1)

            # 解决ip验证问题
            elif '当前IP地址可能存在异常访问行为，完成验证后即可正常使用' in html:
                self.browser.find_element_by_css_selector(".btn").click()
                captcha_element = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.geetest_widget')))
                loc = captcha_element.location
                size = captcha_element.size
                left, top, right, bottom = loc['x'], loc['y'], loc['x'] + size['width'], loc['y'] + size['height']
                # 设置浏览器窗口宽高
                width = self.browser.execute_script('return document.documentElement.scrollWidth')
                height = self.browser.execute_script('return document.documentElement.scrollHeight')
                self.browser.set_window_size(width, height)
                screenshot = self.browser.get_screenshot_as_png()
                screenshot = Image.open(screenshot)
                captcha = screenshot.crop((left, top, right, bottom))
                captcha_bytes = captcha.tobytes()
                result_str = ZhaopinDownloaderMiddleware.base64_api('xxx', 'xxx', captcha_bytes)
                print(result_str)
                for cor in result_str.split('|'):
                    x, y = cor.split(',')
                    ActionChains(self.browser).move_to_element_with_offset(captcha_element, int(x), int(y)).click().perform()
                    time.sleep(.3)
                # 点击确认
                self.browser.find_element_by_css_selector('.geetest_commit_tip').click()
                time.sleep(1)
            return HtmlResponse(url=request.url, body=html, status=200, encoding='utf-8')
        return None

    @staticmethod
    def base64_api(uname, pwd, img: bytes, typeid=21):
        # 请求快识别平台
        b64 = base64.b64encode(img).decode('utf8')
        data = {"username": uname, "password": pwd, "typeid": typeid, "image": b64}
        result = json.loads(requests.post("http://api.ttshitu.com/predict", json=data).text)
        if result['success']:
            return result["data"]["result"]
        else:
            return result["message"]

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
