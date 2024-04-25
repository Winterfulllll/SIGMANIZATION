from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models.gigachat import GigaChat
from urllib.parse import quote
import requests

chat = GigaChat(model="GigaChat-Pro", credentials="NzE1OTQ2YTMtY2FhZC00YzM5LWE3M2EtY2I0Y2U4ZmM0YjMyOjM2ODYxMzhiLWFlYTYtNDliZi1iZjMzLTBjMjViNGRiZGEyYg==", verify_ssl_certs=False)
headers = {
    "accept": "application/json",
    "X-API-KEY": "S2F7CKC-CTEMPQ1-K4YDW4W-NJRG7KH"
}
messages = [
    SystemMessage(
        content="Ты рекомендатор фильмов. Выводи по 10 рекомендованных фильмов на основе любимых жанров в формате: 1. Название@Краткое_содержание@Год_выхода_фильма. Без заголовка."
    )
]

def get_film_id(film_name, year=""):
    url = f"https://api.kinopoisk.dev/v1.4/movie/search?page=1&limit=10&selectFields=id&year={year}"
    encoded_query_text = quote(film_name, encoding='utf-8')
    url += f"&query={encoded_query_text}"
    response = requests.get(url, headers=headers).json()
    return response["docs"][0]["id"]

res = []
favourite_genres = input().split(",")
messages.append(HumanMessage(content=", ".join(favourite_genres)))
print(res_str := chat(messages).content)
res_strs = list(filter(lambda x: x != "", res_str.split("\n")))
for film in res_strs:
    if film.split("@")[0][0].isdigit():
        name_film = film.split("@")[0].split(". ")[1].strip('"').strip("'")
    else:
        name_film = film.split("@")[0].strip('"').strip("'")
    res.append([name_film, film.split("@")[1], get_film_id(name_film, film.split("@")[2])])
print(res)
