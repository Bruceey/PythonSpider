from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

url_set = set()
start_url = 'https://www.toutiao.com/'

options = webdriver.ChromeOptions()
# 处理证书错误
options.add_argument('--ignore-certificate-errors')
# 修改windows.navigator.webdriver，防机器人识别机制，selenium自动登陆判别机制
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_argument("--disable-blink-features=AutomationControlled")

browser = webdriver.Chrome(options=options)

wait = WebDriverWait(browser, 10)
browser.get(start_url)
input_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.main-search .search>input')))
input_element.send_keys("208万日薪")
input_element.send_keys(Keys.ENTER)

time.sleep(5)
print(browser.page_source)

# 获取信息链接
# wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.cs-view .text-xl>a')))
# aElements = browser.find_elements_by_css_selector('.cs-view .text-xl>a')
# for a in aElements:
#     url_set.add(a.get_attribute('href'))
#
# print(url_set)