import requests
from urllib.parse import urlencode, unquote, urljoin
from fake_useragent import UserAgent
import parsel
import csv
import logging
from queue import Queue
from threading import Thread
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')


class TouTiao:
    def __init__(self, keyword, filename='头条新闻.csv'):
        self.fileObj = open(filename, 'w', encoding='utf8')
        self.writer = csv.writer(self.fileObj)
        self.params = {
            'dvpf': 'pc',
            'page_num': '0',
            'keyword': keyword,
            'pd': 'information',
            'source': 'input',
        }
        self.search_url = 'https://so.toutiao.com/search'
        self.base_url = 'https://so.toutiao.com/'
        self.browser = self.get_broswer()
        self.detail_urls = []
        self.page_urls = []

    @staticmethod
    def get_proxy():
        return requests.get("http://127.0.0.1:5010/get/").json()

    def get_broswer(self) -> webdriver:
        options = webdriver.ChromeOptions()
        # 处理证书错误
        options.add_argument('--ignore-certificate-errors')
        # 修改windows.navigator.webdriver，防机器人识别机制，selenium自动登陆判别机制
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_argument("--disable-blink-features=AutomationControlled")
        # 添加代理
        # proxy = TouTiao.get_proxy().get("proxy")
        # options.add_argument('--proxy-server=http://' + proxy)
        browser = webdriver.Chrome(options=options)
        return browser

    def request_start_page_url(self):
        useragent = UserAgent().random
        headers = {
            'User-Agent': useragent,
            'Referer': 'https://so.toutiao.com/',
        }
        r = requests.get(self.search_url, params=self.params, headers=headers)
        html = r.text
        self.parse_links(html, self.search_url, useragent, r.cookies)

    def request_page_url(self):
        print(f"此时page_urls的大小为：{len(self.page_urls)}")
        while len(self.page_urls) != 0:
            page_url, referer = self.page_urls.pop()
            useragent = UserAgent().random
            headers = {
                'User-Agent': useragent,
                'Referer': referer,
            }
            logging.info(f'正在请求： {page_url}')
            r = requests.get(page_url, headers=headers)
            self.parse_links(r.text, page_url, useragent, r.cookies)


    def parse_links(self, html, referer, useragent, cookies):
        sel = parsel.Selector(html)
        hrefs = sel.css('.text-xl>a::attr(href)').re(r'url=(.*)')  # 注意该url已被加密
        print("文章链接: ", [unquote(href) for href in hrefs])

        for href in hrefs:
            item = (unquote(href), referer, useragent, cookies)
            logging.info('添加detail_urls中： (%s, %s, %s, %s)' % item)
            self.detail_urls.append(item)

        # 获取下一页的url，次url从/search开始
        next_page = sel.xpath('//a[contains(.,"下一页")]/@href').get()
        # 下一页的链接
        print('下一页的链接', next_page)
        if next_page:
            item2 = (urljoin(self.base_url, next_page), referer)
            logging.info('添加page_urls中： (%s, %s)' % item2)
            self.page_urls.append(item2)

    def request_article_url(self):
        print(f"此时detail_urls的大小为：{len(self.detail_urls)}")
        while len(self.detail_urls) != 0:
            detail_url, referer, useragent, cookies = self.detail_urls.pop()
            # headers['Referer'] = referer
            # headers['User-Agent'] = useragent
            # logging.info(f'请求文章{detail_url}')
            # r = requests.get(detail_url, headers=headers, cookies=cookies)
            # parse_article(r.text)

            # 利用selenium抓取
            logging.info(f'请求文章{detail_url}')
            self.browser.get(detail_url)
            wait = WebDriverWait(self.browser, 5)
            try:
                wait.until(EC.presence_of_element_located((By.XPATH, '//article')))
                html = self.browser.page_source
                # if 'error' in html:
                #     self.put_back(detail_url, referer, useragent, cookies)
                #     continue
                item = (detail_url, referer, useragent, cookies)
                self.parse_article(html, item)
            except TimeoutException as e:
                logging.error(e)
                self.put_back(detail_url, referer, useragent, cookies)


    def parse_article(self, html, item):
        sel = parsel.Selector(html)
        title = sel.css('h1::text').get()
        article = sel.xpath('//article//text()').extract()
        if not title or not article:
            return self.put_back(*item)
        article = ''.join(article)

        row = [title, article]
        print(f'保存当清数据{row}')
        self.writer.writerow(row)

    def put_back(self, detail_url, referer, useragent, cookies):
        self.browser.close()
        self.browser = self.get_broswer()
        # 放回原队列
        self.detail_urls.insert(0, (detail_url, referer, useragent, cookies))

    def start(self):
        self.request_start_page_url()
        # while len(self.page_urls) != 0:
        #     self.request_page_url()
        # while len(self.detail_urls) != 0:
        #     self.request_article_url()
        self.request_article_url()


    def __del__(self):
        self.fileObj.close()
        self.browser.close()


if __name__ == '__main__':
    toutiao = TouTiao('208万日薪')
    toutiao.start()
