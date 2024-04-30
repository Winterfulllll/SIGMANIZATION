from langchain.schema import HumanMessage, SystemMessage
from configuration import giga, app_config as config
from flask import jsonify
import requests

our_header = {
    'API-KEY': config["SECRET_KEY"]
}

films_header = {
    'X-API-KEY': config["MOVIES_API"]
}


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
    """
    Generates a list of recommended film IMDB IDs for a given user using their preferences and past reviews.

    Args:
        username (str): The username of the user for whom to generate recommendations.
        count (int): The number of film recommendations to generate.

    Returns:
        str: A JSON string containing a list of recommended film IMDB IDs.
    """
    prompt = SystemMessage(
        content="Ты - полезный помощник с искусственным интеллектом, обладающий обширными знаниями о фильмах." +
        "Я предоставлю тебе какие фильмы нравятся пользователю и какие оценки он оставлял различным фильмам." +
        f"Ты на их основе сгенерируй список только уникальных IMDB ID рекомендованных данному пользователю фильмов, в количестве {count} в формате JSON")
    text = ""

    response = requests.get(
        url=f"http://127.0.0.1:8000/api/preferences/{username}",
        headers=our_header
    ).json()
    for preference in response:
        text += f'{preference["type"]}:{preference["type_value"]},\n'
    response = requests.get(
        url=f"http://127.0.0.1:8000/api/reviews/{username}",
        headers=our_header
    ).json()
    for review in response:
        film_response = requests.get(
            url=f'https://api.kinopoisk.dev/v1.4/movie/{
                review["item_id"]}&selectFields=name',
            headers=films_header
        ).json()
        film_name = film_response["docs"]["name"]
        text += f'{film_name}:{review["rating"]},\n'

    print(text)
    human_message = HumanMessage(content=text)
    response = giga([prompt, human_message])
    print(response.content)
    return jsonify(response.content)
