from scrapy.loader import ItemLoader
from scrapy.loader.processors import Compose


def serialize(self, value):
    if value == '' or value == None:
        return ''
    else:
        return str(value).strip()


class LianJiaLoader(ItemLoader):
    default_input_processor = Compose(serialize)
