import requests
from fake_useragent import UserAgent
import csv

ua = UserAgent(verify_ssl=False)
import parsel

start_url = 'https://www.lianjia.com/city/'
headers = {
    'referer': 'https://www.lianjia.com/',
}


def request_url(url):
    headers['user-agent'] = ua.random
    try:
        r = requests.get(url, timeout=5)
        return r.text
    except Exception as e:
        print(e)


start_html = request_url(start_url)
sel = parsel.Selector(start_html)
city_list = sel.css('.city_list')


fp = open('urls.csv', 'w')
writer = csv.writer(fp)
try:
    for city_info in city_list:
        # 中文省份
        provice = city_info.css('.city_list_tit::text').get()
        # 该省份所有的中文城市名字和链接
        cities = city_info.css('ul>li a::text').extract()
        city_links = city_info.css('ul>li a::attr(href)').extract()
        for i in range(len(cities)):
            writer.writerow([provice, cities[i], city_links[i]])
finally:
    fp.close()

