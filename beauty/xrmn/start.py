from scrapy import cmdline

if __name__ == '__main__':
    # scrapy crawl somespider -s JOBDIR=crawls/somespider-1
    cmdline.execute('scrapy crawl xrmnw'.split())
    # cmdline.execute('scrapy crawl xrmnw -s JOBDIR=crawls/xrmnw'.split())
