from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import parsel


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

url = 'https://www.toutiao.com/a6956102868286112270/?channel=&source=search_tab'
browser.get(url)

wait = WebDriverWait(browser, 20)
wait.until(EC.presence_of_element_located((By.XPATH, '//article')))
sel = parsel.Selector(browser.page_source)
title = sel.css('h1::text').get()
article = sel.xpath('//article//text()').extract()
article = ''.join(article)
print(title)
print(article)