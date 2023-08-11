BOT_NAME = "vc"

SPIDER_MODULES = ["parsers.spiders"]
NEWSPIDER_MODULE = "parsers.spiders"

ROBOTSTXT_OBEY = False

CONCURRENT_REQUESTS = 10

DOWNLOAD_DELAY = 0

COOKIES_ENABLED = True

ITEM_PIPELINES = {
   "parsers.pipelines.VcPipeline": 300,
}

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
FEED_FORMAT = 'json'
FEED_URI = 'vc_temp.json'
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'
LOG_ENABLED = False
LOG_LEVEL = "DEBUG"
