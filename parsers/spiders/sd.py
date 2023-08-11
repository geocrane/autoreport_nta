import json
from datetime import datetime as dt

from parsers.utils import get_date_from

with open("data/response.txt", "r", encoding="utf-8") as f:
    text = f.read()


class SDParser:
    # sd_link = (
    #     "https://habr.com/ru/users/NewTechAudit/posts/page{page_number}/"
    # )
    # article_link = "https://habr.com/ru/articles/{id}/"
    # requestSize = 100
    to_date = get_date_from()
    parsed_data = []

    def get_link(self, page_number):
        return self.sd_link.format(page_number=page_number)

    def parse(self):
        articles_data = text
        articles = json.loads(articles_data)["content"]
        for article in articles:
            date_unix = int(str(article["createdAt"])[:10])
            date = dt.utcfromtimestamp(date_unix).date()
            if date < self.to_date:
                pass
            else:
                try:
                    item = {
                        "site": "SDrug",
                        "title": article["title"].strip(),
                        "date": date.strftime("%d.%m.%Y"),
                        "views": article["viewCount"],
                        "urls": article["link"],
                    }
                    print(f'sd: {item["date"]} -> {item["title"]}')
                    self.parsed_data.append(item)
                except:
                    pass
        return self.parsed_data
