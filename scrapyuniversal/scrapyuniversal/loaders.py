from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join, Compose, TakeFirst


class ChinaLoader(ItemLoader):
    default_output_processor = TakeFirst()
    text_out = Compose(Join(), lambda s: s.strip())
    source_out = Compose(Join(), lambda s: s.strip())
