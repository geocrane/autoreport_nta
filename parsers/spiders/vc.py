from datetime import datetime as dt
import json
import re

import scrapy
from urllib.parse import urlencode

from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from scrapy.selector import Selector

from parsers.items import VcItem
from parsers.utils import get_date_from


class VcruSpider(scrapy.Spider):
    name = "vc"
    allowed_domains = ["vc.ru"]
    start_urls = ["https://vc.ru/newtechaudit/entries/new"]
    main_url = "https://vc.ru/newtechaudit/entries/new/more?"
    page = 2
    date_from = get_date_from()
    stop = False
    parsed_data = []

    def parse(self, response):
        links = response.xpath("//a[@class='content-link']")
        for link in links:
            yield response.follow(link, callback=self.parse_ads)

        last_id, last_sorting_value, exclude_ids = self.get_more_page(response)
        more = self.get_dict_more_page(
            last_id, last_sorting_value, self.page, exclude_ids
        )
        if more["last_sorting_value"] is not None:
            next_page = f"{self.main_url}{urlencode(more)}"
            yield response.follow(next_page, callback=self.get_next_page)

    def parse_ads(self, response):
        date_text = response.xpath("//time[@class='time']/@title").get()
        match = re.search(r"\d{2}.\d{2}.\d{4}", date_text)
        date = dt.strptime(match.group(), "%d.%m.%Y").date()
        if date < self.date_from:
            self.stop = True
            return

        loader = ItemLoader(item=VcItem(), response=response)
        loader.add_value("site", "VC")
        loader.add_xpath("title", "//h1//text()")
        loader.add_xpath("date", "//time[@class='time']/@title")
        loader.add_xpath("views", "//div[@class='post-counters']/@data-hits")
        loader.add_value("urls", response.url)

        title = response.xpath("//h1//text()").get().strip()
        print(f"vc: {date.strftime('%d.%m.%Y')} -> {title}")
        return loader.load_item()

    def get_more_page(self, response):
        try:
            last_sorting_value = (
                response.xpath(
                    "//div[@class='feed']/@data-feed-last-sorting-value"
                )
                .extract_first()
                .replace(",", ".")
            )
        except Exception:
            last_sorting_value = None
        last_id = response.xpath(
            "//div[@class='feed']/@data-feed-last-id"
        ).extract_first()
        exclude_ids = response.xpath(
            "//div[@class='feed']/@data-feed-exclude-ids"
        ).extract_first()
        if exclude_ids is None:
            exclude_ids = ""
        return last_id, last_sorting_value, exclude_ids

    def get_dict_more_page(
        self, last_id, last_sorting_value, page, exclude_ids
    ):
        more = {
            "last_id": str(last_id),
            "last_sorting_value": str(last_sorting_value),
            "page": page,
            "exclude_ids": exclude_ids,
            "mode": "raw",
        }
        return more

    def get_next_page(self, response: HtmlResponse):
        js_file = json.loads(response.text)
        response2 = Selector(text=js_file["data"]["items_html"])
        links = response2.xpath("//a[@class='content-link']")
        for link in links:
            yield response.follow(link, callback=self.parse_ads)
        if not self.stop:
            self.page += 1
            exclude_ids = self.get_more_page(response2)
            if js_file["data"]["last_sorting_value"] is not None:
                more = self.get_dict_more_page(
                    js_file["data"]["last_id"],
                    js_file["data"]["last_sorting_value"],
                    self.page,
                    exclude_ids[2],
                )
                next_page = f"{self.main_url}{urlencode(more)}"
                yield response.follow(next_page, callback=self.get_next_page)
