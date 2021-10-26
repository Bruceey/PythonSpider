# 彼岸网美女图片抓取（多线程版本）
import time
import requests
from bs4 import BeautifulSoup
import os
import atexit
from concurrent.futures import ThreadPoolExecutor

# 程序停止会自动计算下载总时间和下载速度
@atexit.register
def calc_time():
    """
    日志
    :return:
    """
    # 计算下载总时间
    end = time.time()
    duration = end - start
    hour = int(duration / 3600)
    minute = int((duration - hour * 3600) / 60)
    seconds = int(duration - hour * 3600 - minute * 60)

    # 计算下载速度
    size = 0    # 单位是字节
    files = os.listdir("image")
    for file in files:
        try:
            size += os.path.getsize("./image/" + file)
        except Exception as e:
            print(e)
    # 单位是M
    size = size / 1024 / 1024
    # 单位是kb/s
    speed = size * 1024 / duration

    print("\033[31m="*100)
    print("一共下载了{}个文件, 大小为{:.2f}M".format(len(files), size))
    print("下载速度为{:.2f} kb/s".format(speed))
    print("耗时{}小时{}分钟{}秒".format(hour, minute, seconds))
    print("="*100)


headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36',
}


# 请求url，得到html代码
def get_url(url):
    response =  requests.get(url, headers=headers)
    return response.content.decode("gbk")

# 下载图片
def download(url):
    print("正在下载链接地址为 %s 的图片" %url)
    # 二进制文件
    content = requests.get(url, headers=headers).content
    # url的格式 http://img.netbian.com/file/2021/0122/2861bb5516bd41b0dfe79f6a9538892d.jpg
    # 取最后一个"/"之后的字符串作为文件名
    filename = url.split("/")[-1]
    # 拼写完整的图片路径，其中这里的"."表示当前这个文件所在的目录
    file_path = "./image/" + filename
    # 将二进制数据写入文件
    with open(file_path, 'wb') as f:
        f.write(content)

def run(url):
    html = get_url(url)
    # 利用BeautifulSoup构建解析器
    soup = BeautifulSoup(html, "lxml")

    # 选取所有的图片所在的块区域
    aElements = soup.select('.list a')
    hrefs = [i["href"] for i in aElements]

    for href in hrefs:
        if href.startswith("/desk"):
            # url2是缩略图对应的链接
            url2 = "http://www.netbian.com" + href

            # 请求缩略图链接得到页面内容
            html2 = get_url(url2)
            soup2 = BeautifulSoup(html2, "lxml")
            src = soup2.select('.pic img')[0]["src"]
            download(src)

if __name__ == '__main__':
    start = time.time()

    # 判断当前目录下是否有image文件夹，没有就创建
    if not os.path.exists("image"):
        os.mkdir("image")

    try:
        with ThreadPoolExecutor() as pool:
            # 此处是下载的页数，可自行更改
            for page in range(1, 51):
                if page == 1:
                    url = 'http://www.netbian.com/meinv/'
                else:
                    url = 'http://www.netbian.com/meinv/index_%d.htm' % page
                pool.submit(run, url)
    except Exception as e:
        print(f'\033[31m{e}')
        print("\33[0m")