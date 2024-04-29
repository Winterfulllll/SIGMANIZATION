from langchain.schema import HumanMessage, SystemMessage
from configuration import giga
import requests


def generate_film_plot(film: str) -> str:
    """
    Generates a film plot using GigaChat.

    Args:
        film (str): The name of the film.

    Returns:
        str: The generated film plot.
    """
    prompt = SystemMessage(
        content="Ты - полезный помощник с искусственным интеллектом, обладающий обширными знаниями о фильмах. Я сообщу тебе название фильма, а ты кратко изложишь сюжет.")
    human_message = HumanMessage(content=f"Какой сюжет у фильма: {film}")
    response = giga([prompt, human_message])
    plot = response.content
    return plot


def generate_recommended_films(username: str, count: int):
    prompt = SystemMessage(
        content="Ты - полезный помощник с искусственным интеллектом, обладающий обширными знаниями о фильмах.Э" +
        "Я предоставлю тебе какие фильмы нравятся пользователю и какие оценки он оставлял различным фильмам." +
        f"А ты на их основе сгенерируй список только IMDB ID рекомендованных данному пользователю фильмов, в количестве {count} в формате JSON")
    text = ""

    response = requests.get(
        url=f"http://127.0.0.1:8000/api/preferences/{username}").json()
    for preference in response:
        text += f"{preference["type"]}:{preference["type_value"]},\n"
    response = requests.get(
        url=f"http://127.0.0.1:8000/api/reviews/{username}").json()
    for review in response:
        film_response = requests.get(
            url=f"https://api.kinopoisk.dev/v1.4/movie/{review["item_id"]}&selectFields=name").json()
        film_name = film_response["docs"]["name"]
        text += f"{film_name}:{review["rating"]},\n"

    human_message = HumanMessage(content=text)
    response = giga([prompt, human_message])
    return response.content
