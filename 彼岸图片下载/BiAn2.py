# 彼岸网整站爬取
import requests
from bs4 import BeautifulSoup
import os


headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36',
}

# 请求url，得到html代码
def get_url(url):
    response =  requests.get(url, headers=headers)
    return response.content.decode("gbk")

# 下载图片
def download(url, category):
    print("正在下载 %s 分类下链接地址为 %s 的图片" %(category, url))
    # 二进制文件
    content = requests.get(url, headers=headers).content
    # url的格式 http://img.netbian.com/file/2021/0122/2861bb5516bd41b0dfe79f6a9538892d.jpg
    # 取最后一个"/"之后的字符串作为文件名
    filename = url.split("/")[-1]

    # 拼写完整的图片路径，其中这里的"."表示当前这个文件所在的目录
    file_path = "./%s/" %category + filename          # 目录改为category这个变量
    # 将二进制数据写入文件
    with open(file_path, 'wb') as f:
        f.write(content)

def main():
    # 为了程序的完整性，加一个try
    try:

        # 1、获取所有分类
        start_url = 'http://www.netbian.com/'
        start_html = get_url(start_url)
        start_soup = BeautifulSoup(start_html, "lxml")

        # 2、查找分类和对应的链接
        start_aElements = start_soup.select(".nav.cate>a")
        categories = [i.string for i in start_aElements]
        links = ["http://www.netbian.com" + i["href"] for i in start_aElements]
        categories_links = list(zip(categories, links))[1:]

        for category, link in categories_links:
            # 判断当前目录下是否有category文件夹，没有就创建
            if not os.path.exists(category):
                os.mkdir(category)

            # 先请求每个分类的主页，获取总共的页数
            category_homepage_html = get_url(link)
            page_soup = BeautifulSoup(category_homepage_html, "lxml")
            pageElement = page_soup.select('.page>a')[-2]
            totalPage = int(pageElement.string)


            # 之前的代码
            for page in range(1, totalPage+1):   # 这个数改为totalPage+1
                if page == 1:
                    url = link
                else:
                    url = link + "index_%d.htm" % page

                print("正在请求 %s" % url)
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
                        download(src, category)            # 加上category分类


    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()