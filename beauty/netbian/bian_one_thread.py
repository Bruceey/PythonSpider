import requests
import parsel
from urllib.parse import urljoin

import os

image_store = r"C:\Users\17634\Desktop\bian2"
os.makedirs(image_store, exist_ok=True)

start_urls = ["http://www.netbian.com/meinv/",
              # "http://www.netbian.com/meinv/index_2.htm"
              ]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',

}

import time
time1 = time.time()

for start_url in start_urls:
    r = requests.get(start_url, headers=headers)
    html = r.text
    sel = parsel.Selector(html)
    image_urls = sel.css('.list li a::attr(href)').extract()
    headers['Referer'] = start_url
    for url in image_urls:
        if not url.startswith('http:'):
            url = urljoin(start_url, url)
            r = requests.get(url, headers=headers)
            sel = parsel.Selector(r.text)
            image_src = sel.css('.pic img::attr(src)').get()
            headers['Referer'] = url
            r = requests.get(image_src, headers=headers)
            image_bytes = r.content
            filename = image_src.split('/')[-1]
            with open(os.path.join(image_store, filename), 'wb') as f:
                f.write(image_bytes)

time2 = time.time()

print(f"耗时: {time2 - time1} s")