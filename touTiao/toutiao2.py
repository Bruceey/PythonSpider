import requests
from urllib.parse import urlencode, unquote, urljoin
from fake_useragent import UserAgent
import parsel
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
import csv
import logging
import threading

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


# def get_proxy():
#     return requests.get("http://127.0.0.1:5010/get/").json()


def get_broswer() -> webdriver:
    global browser
    options = webdriver.ChromeOptions()
    # 处理证书错误
    options.add_argument('--ignore-certificate-errors')
    # 修改windows.navigator.webdriver，防机器人识别机制，selenium自动登陆判别机制
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_argument("--disable-blink-features=AutomationControlled")
    # 添加代理
    # proxy = get_proxy().get("proxy")
    # options.add_argument('--proxy-server=http://' + proxy)
    browser = webdriver.Chrome(options=options)
    return browser

# 获取browser
browser = get_broswer()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
base_url = 'https://so.toutiao.com/'

ua = UserAgent()
filename = '头条新闻.csv'
file = open(filename, 'w', encoding='utf8')
writer = csv.writer(file)
# print(type(ua.random))
# print(ua.random)

headers = {
    'User-Agent': None,
    'Referer': 'https://so.toutiao.com/',
}

query = {
    'dvpf': 'pc',
    'page_num': '0',
    'keyword': '208万日薪',
    'pd': 'information',
    'source': 'input',
}
search_url = 'https://so.toutiao.com/search?' + urlencode(query)

detail_urls = Queue()
page_urls = Queue()

keyword = None


def request_start_page_url():
    query['keyword'] = keyword
    useragent = ua.random
    headers['User-Agent'] = useragent
    r = requests.get(search_url, headers=headers)
    html = r.text
    parse_links(html, search_url, useragent, r.cookies)


def request_page_url():
    print('进入request_page_url')
    print(page_urls.qsize())
    while not page_urls.empty():
        page_url, referer = page_urls.get()
        headers['Referer'] = referer
        useragent = ua.random
        headers['User-Agent'] = useragent
        logging.info(f'正在请求： {page_url}')
        r = requests.get(page_url, headers=headers)
        parse_links(r.text, page_url, useragent, r.cookies)
        page_urls.task_done()


def parse_links(html, url, useragent, cookies):
    sel = parsel.Selector(html)
    hrefs = sel.css('.text-xl>a::attr(href)').re(r'url=(.*)')  # 注意该url已被加密
    print("文章链接: ", [unquote(href) for href in hrefs])
    for href in hrefs:
        item = (unquote(href), url, useragent, cookies)
        logging.info('添加detail_urls中： (%s, %s, %s, %s)' % item)
        detail_urls.put_nowait(item)

    # 获取下一页的url，次url从/search开始
    next_page = sel.xpath('//a[contains(.,"下一页")]/@href').get()
    # 下一页的链接
    print('下一页的链接', next_page)
    if next_page:
        item2 = (urljoin(base_url, next_page), url)
        logging.info('添加page_urls中： (%s, %s)' % item2)
        page_urls.put_nowait(item2)
    print('开始请求时刚放入队列中')
    print(page_urls.qsize())
    print(detail_urls.qsize())


def request_article_url():
    print('进入request_article_url')
    print(f'detail_urls的大小 {detail_urls.qsize()}')
    while not detail_urls.empty():
        detail_url, referer, useragent, cookies = detail_urls.get()
        # headers['Referer'] = referer
        # headers['User-Agent'] = useragent
        # logging.info(f'请求文章{detail_url}')
        # r = requests.get(detail_url, headers=headers, cookies=cookies)
        # parse_article(r.text)

        # 利用selenium抓取
        logging.info(f'请求文章{detail_url}')
        browser.get(detail_url)
        wait = WebDriverWait(browser, 20)
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, '//article')))
            html = browser.page_source
            if 'error' in html:
                put_back(detail_url, referer, useragent, cookies)
                detail_urls.task_done()
                continue
            parse_article(html)
        except TimeoutException as e:
            logging.error(e)
            put_back(detail_url, referer, useragent, cookies)
        detail_urls.task_done()


def put_back(detail_url, referer, useragent, cookies):
    get_broswer()
    # 放回原队列
    detail_urls.put_nowait((detail_url, referer, useragent, cookies))


def parse_article(html):
    sel = parsel.Selector(html)
    title = sel.css('h1::text').get()
    article = sel.xpath('//article//text()').extract()
    article = ''.join(article)

    row = [title, article]
    print(f'保存当清数据{row}')
    writer.writerow(row)


def process_thread(t):
    # 设置守护进程
    t.daemon = True
    t.start()


def main():
    global keyword
    keyword = '208万日薪'
    # 起始爬取
    request_start_page_url()


    request_page_url_thread = threading.Thread(target=request_page_url)
    request_detail_url = threading.Thread(target=request_article_url)
    with ThreadPoolExecutor(3) as pool:
        pool.map(process_thread, [request_page_url_thread, request_detail_url])
        page_urls.join()
        detail_urls.join()
    file.close()


if __name__ == '__main__':
    main()
