from scrapy.logformatter import *
import hashlib


def decorator(func):
    def wrapper(*args, **kwargs):
        obj = args[0]
        item = dict(args[1])
        item['image_bytes'] = hashlib.sha1(item['image_bytes']).hexdigest()
        return func(obj, item, *args[2:])
    return wrapper


class MyLogFormatter(LogFormatter):
    @decorator
    def scraped(self, item, response, spider):
        return super().scraped(item, response, spider)

    @decorator
    def dropped(self, item, exception, response, spider):
        return super().dropped(item, exception, response, spider)

    @decorator
    def item_error(self, item, exception, response, spider):
        return super().item_error(item, exception, response, spider)
