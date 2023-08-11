import requests
import json

from fake_useragent import UserAgent
from bs4 import BeautifulSoup as bs


class HabrParser:
    habr_link = (
        "https://habr.com/ru/users/NewTechAudit/posts/page{page_number}/"
    )
    start_page = 1
    to_date = 

    def get_link(self, page_number):
        return self.habr_link.format(page_number=page_number)

    def habr_parsing(self):
        response = requests.get(
            self.get_link(self.start_page),
            headers={"User-Agent": UserAgent().chrome},
        )
        soup = bs(response.content, "html.parser")
        articles_data = soup.html.body.script.text.split("(function()")[0][25:-1]
        articles = json.loads(articles_data)["articlesList"]["articlesList"]
        for article in articles.values():
            print(
                f'{article["timePublished"]} -> {article["titleHtml"]} -> просмотров: {article["statistics"]["readingCount"]}'
            )


print(HabrParser().habr_parsing())
