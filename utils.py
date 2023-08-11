import datetime as dt
import json
import os

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

import settings
from normalizator import Normalizator


def parse_json(filename):
    with open(filename, "r", encoding="utf-8") as file:
        dictionary = json.load(file)
    for element in dictionary:
        element["views"] = int(element["views"])
    os.remove(filename)
    return dictionary


def filter_reestr(reestr_file):
    reestr_df = pd.read_excel(reestr_file)
    filtered_reestr = reestr_df[
        reestr_df["Промежуточный статус"] == "16. Пост готов"
    ][
        [
            "ID Сервис NTA",
            "ТБ",
            "Название поста",
            "Дата добавления",
            "ТБ (Эксперт 1)",
            "ТБ (Эксперт 2)",
            "Редактор (ЦК)",
        ]
    ]
    with pd.ExcelWriter("data/filtered_reestr.xlsx") as writer:
        filtered_reestr.to_excel(writer, index=False)


def extract_date_from_xlsx_string(filename, format):
    return dt.datetime.strptime(filename.split("_")[1][:-5], format).date()


def get_last_file_path(dir_path):
    files = os.listdir(dir_path)
    sorted_by_date = sorted(
        files, key=lambda x: os.path.getctime(os.path.join(dir_path, x))
    )
    return dir_path + sorted_by_date[-1]


def get_from_file_path(dir_path):
    files = os.listdir(dir_path)
    for days in reversed(range(1, settings.NEWS_FROM + 1)):
        for file in files:
            file_date = extract_date_from_xlsx_string(
                file, settings.XLSX_DATE_FORMAT
            )
            if file_date == dt.date.today() - dt.timedelta(days=days):
                return dir_path + file
    return get_last_file_path(dir_path)


def get_dataframes_for_compare(dir_path):
    last_file = get_last_file_path(dir_path)
    from_file = get_from_file_path(dir_path)
    last_date = extract_date_from_xlsx_string(
        last_file, settings.XLSX_DATE_FORMAT
    )
    from_date = extract_date_from_xlsx_string(
        from_file, settings.XLSX_DATE_FORMAT
    )
    print(f"{from_date} <=> {last_date}")
    previous = pd.read_excel(from_file)
    last = pd.read_excel(last_file)
    return last, previous


def get_new_rows(new, old):
    new_rows = new.merge(
        old, on=["title", "site"], how="outer", indicator=True
    )
    new_rows = new_rows[new_rows["_merge"] == "left_only"]
    return new_rows


def get_article_by_id(id, reestr):
    filtered_reestr = pd.read_excel(reestr)
    article = filtered_reestr[filtered_reestr["ID Сервис NTA"] == id]
    return article


def smart_strings_compare():
    norm = Normalizator()
    last, previous = get_dataframes_for_compare(settings.RESULTS_DIR)
    df_nta = get_new_rows(last, previous)
    if not len(df_nta) > 0:
        return False
    nta_titles = df_nta["title"]
    df_reestr = pd.read_excel("data/export_articles.xlsx")
    df_reestr = df_reestr[
        df_reestr["status"] != "Отклонено"
    ]
    reestr_titles = df_reestr["article_name"]

    results = []
    for nta_title in nta_titles:
        corpus = [nta_title]
        for str in reestr_titles:
            corpus.append(str)

        tfIdfVectorizer = TfidfVectorizer(use_idf=True, stop_words=["english"])
        X = tfIdfVectorizer.fit_transform(norm.normalize_list(corpus))

        vector_str2 = X.toarray()[0]
        vector1Len = np.linalg.norm(vector_str2)
        coef = 0
        article = ""
        for index, vector in enumerate(X.toarray()[1:]):
            numerator = np.dot(vector_str2, vector)
            vector2Len = np.linalg.norm(vector)
            denominator = vector1Len * vector2Len
            np.seterr(divide="ignore", invalid="ignore")
            cosine = numerator / denominator
            pub_title = corpus[0]
            if cosine > coef:
                coef = round(cosine, 2)
                article = corpus[index + 1]


        article_id = df_reestr[df_reestr["article_name"] == article]["id"]
        article_id_value = article_id.loc[article_id.index[0]]

        site = df_nta[df_nta["title"] == pub_title]["site"]
        site_value = site.loc[site.index[0]]

        date_pub = df_nta[df_nta["title"] == pub_title]["date_x"]
        date_pub_value = date_pub.loc[date_pub.index[0]]

        filtered_article = get_article_by_id(
            article_id_value, "data/filtered_reestr.xlsx"
        )
        filtered_article["nta_id"] = [article_id_value]
        filtered_article["public_title"] = [pub_title]
        filtered_article["coef"] = [coef]
        filtered_article["reestr_name"] = [article]
        filtered_article["site"] = site_value
        filtered_article["date_pub"] = date_pub_value
        filtered_dict = filtered_article.to_dict(orient="list", index=True)
        results.append(filtered_dict)

    res = pd.DataFrame(results)

    res["site"] = res["site"].str[0]
    res["ID Сервис NTA"] = res["ID Сервис NTA"].str[0]
    res["ТБ"] = res["ТБ"].str[0]
    res["Название поста"] = res["Название поста"].str[0]
    res["date_pub"] = res["date_pub"].str[0]
    res["ТБ (Эксперт 1)"] = res["ТБ (Эксперт 1)"].str[0]
    res["ТБ (Эксперт 2)"] = res["ТБ (Эксперт 2)"].str[0]
    res["Редактор (ЦК)"] = res["Редактор (ЦК)"].str[0]
    res["nta_id"] = res["nta_id"].str[0]
    res["public_title"] = res["public_title"].str[0]
    res["coef"] = res["coef"].str[0]
    res["reestr_name"] = res["reestr_name"].str[0]
    res["Дата добавления"] = res["Дата добавления"].str[0]
    res["Дата добавления"] = pd.to_datetime(res["Дата добавления"])

    res = res[
        [
            "site",
            "nta_id",
            "ТБ",
            "reestr_name",
            "date_pub",
            "ТБ (Эксперт 1)",
            "ТБ (Эксперт 2)",
            "Редактор (ЦК)",
            "coef",
            "public_title",
            "ID Сервис NTA",
            "Название поста",
            "Дата добавления"
        ]
    ]

    res["date_pub"] = pd.to_datetime(res["date_pub"], format="%d.%m.%Y")
    res = res.sort_values(["site", "date_pub"], ascending=[False, True])
    res["date_pub"] = res["date_pub"].dt.strftime("%d.%m.%Y")

    with pd.ExcelWriter("data/news.xlsx") as writer:
        res.to_excel(writer, index=False)

    return True
