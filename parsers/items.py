import scrapy
from itemloaders.processors import TakeFirst


class VcItem(scrapy.Item):
    site = scrapy.Field(output_processor=TakeFirst())
    title = scrapy.Field(output_processor=TakeFirst())
    date = scrapy.Field(output_processor=TakeFirst())
    views = scrapy.Field(output_processor=TakeFirst())
    urls = scrapy.Field(output_processor=TakeFirst())
