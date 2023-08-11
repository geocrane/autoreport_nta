import requests
import json
from datetime import datetime as dt

from fake_useragent import UserAgent
from bs4 import BeautifulSoup as bs

from parsers.utils import get_date_from


class HabrParser:
    habr_link = (
        "https://habr.com/ru/users/NewTechAudit/posts/page{page_number}/"
    )
    article_link = "https://habr.com/ru/articles/{id}/"
    page = 1
    to_date = get_date_from()
    parsed_data = []
    stop = False

    def get_link(self, page_number):
        return self.habr_link.format(page_number=page_number)

    def parse(self):
        response = requests.get(
            self.get_link(self.page),
            headers={"User-Agent": UserAgent().chrome},
        )
        soup = bs(response.content, "html.parser")
        articles_data = soup.html.body.script.text.split("(function()")[0][
            25:-1
        ]
        articles = json.loads(articles_data)["articlesList"]["articlesList"]
        for article in articles.values():
            date_text = article["timePublished"][:10]
            date = dt.strptime(date_text, "%Y-%m-%d").date()
            if date < self.to_date:
                self.stop = True
                pass
            else:
                item = {
                    "site": "Habr",
                    "title": article["titleHtml"].strip(),
                    "date": date.strftime("%d.%m.%Y"),
                    "views": article["statistics"]["readingCount"],
                    "urls": self.article_link.format(id=article["id"]),
                }
                print(f'habr: {item["date"]} -> {item["title"]}')
                self.parsed_data.append(item)
            if not self.stop:
                self.page += 1
                self.parse()
        return self.parsed_data
