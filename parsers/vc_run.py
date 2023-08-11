from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from parsers import settings
from parsers.spiders.vc import VcruSpider


def vc_parse():
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(VcruSpider)
    process.start()
