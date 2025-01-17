# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
import os
import logging
from scrapy import Request
from scrapy.http.request import NO_CALLBACK
from pathlib import Path
import re


class MntucePipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None, *, item) -> str:
        url = request.url
        actress = item["actress"]
        album_name = item["album_name"]
        filename = url.rsplit("/", 1)[-1].rsplit(".", 1)[0]
        try:
            filename = filename.split("-")[0]
        except Exception as e:
            logging.exception(e)
        return f"{actress}/{album_name}_{filename}.jpg"

    def get_media_requests(self, item, info):
        urls = ItemAdapter(item).get(self.images_urls_field, [])
        for u in urls:
            r = Request(u, callback=NO_CALLBACK)
            r.headers["Referer"] = item["referer"]
            yield r

    def close_spider(self, spider):
        with open("overall.txt", "w") as f:
            photo_nums = 0
            f.write(getattr(spider, "overall_info"))
            for path in Path(f"{spider.record}/{spider.actress}").iterdir():
                if path.name != ".DS_Store" and path.is_file():
                    album_link = path.read_text()
                    f.write(f"{path.name}  {album_link}\n")
                    # 累加照片总数
                    n = re.search(r"\[(\d+).\]", path.name)
                    if n:
                        photo_nums += int(n.group(1))

            overall_page = re.search(r"共(\d+)篇", spider.overall_info)
            if overall_page:
                photo_nums_max = photo_nums + int(overall_page.group(1))
                message = f"照片总共大约有[{photo_nums}, {photo_nums_max}]"
                f.write(message)
            else:
                message = f'照片总共有{photo_nums}'
                f.write(message)
        logging.info("计算得到: " + message)
            

        # import shutil
        # shutil.rmtree('./spider.record')
