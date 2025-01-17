from scrapy import cmdline
import os


if __name__ == '__main__':
    os.chdir(os.path.dirname(__file__))
    cmdline.execute('scrapy crawl xiuren'.split())
    # cmdline.execute('scrapy crawl test'.split())
