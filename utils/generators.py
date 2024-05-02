from langchain.schema import HumanMessage, SystemMessage
from flask import abort
from configuration import giga, app_config as config
from utils.preferences import get_preference
from utils.reviews import get_review
import requests
import json


def generate_film_plot(film: str) -> str:
    """
    Generates a film plot using GigaChat.

    Args:
        film (str): The name of the film.

    Returns:
        str: The generated film plot.
    """
    try:
        prompt = SystemMessage(
            content="Ты - полезный помощник с искусственным интеллектом, обладающий обширными знаниями о фильмах. " +
                    "Я сообщу тебе название фильма или его IMDB ID, а ты кратко изложишь сюжет. " +
                    "Ответ должен быть в HTML формате")
        human_message = HumanMessage(content=f"Какой сюжет у фильма: {film}")
        response = giga([prompt, human_message])
        plot = {"plot": response.content}
        return plot

    except Exception as e:
        return {"error": str(e)}, 500


def generate_recommended_films(username: str, count: int):
    """
    Generates a list of recommended film IMDB IDs for a given user using their preferences and past reviews.

    Args:
        username (str): The username of the user for whom to generate recommendations.
        count (int): The number of film recommendations to generate.

    Returns:
        str: A JSON string containing a list of recommended film IMDB IDs.
    """
    try:
        if count < 1 or count > 20:
            return abort(400, "Invalid count value (must be between 1 and 20)")

        prompt = SystemMessage(
        content=f"Ты рекомендатор фильмов. Выведи {count} штук рекомендованных фильмов на основе предпочтений пользователя в формате: 1. Название. Без заголовка."
    )
        text = f"Предпочтения пользователя:\n"

        for preference in get_preference(username):
            text += f'- {preference["type"]}: {preference["type_value"]}\n'

        text += "\nОценки пользователя:\n"
        for review in get_review(username):
            rating = review["rating"]
            if rating:
                film_response = requests.get(
                    url=f'''https://api.kinopoisk.dev/v1.4/movie?externalId.imdb={review["item_id"]}&selectFields=name''',
                    headers={"accept": "application/json", 'X-API-KEY': config["MOVIES_API"]}
                ).json()
                if film_response["total"] != 0:
                    text += f'''- "{film_response['docs']
                                    [0]['name']}": {rating},\n'''

        res_names = []
        human_message = HumanMessage(content=text)
        response = giga([prompt, human_message])
        recommended_films = list(filter(lambda x: x != "", response.content.split("\n")))
        for film in recommended_films:
            film_name = film.split(". ")[1].strip('"').strip("'")
            res_names.append(film_name)

        attempts = 0
        while len(res_names) < count:
            human_message = HumanMessage(content=f"Сгенируй еще {count} штук фильмов!\n" + text)
            response = giga([prompt, human_message])
            recommended_films = list(filter(lambda x: x != "", response.content.split("\n")))
            for film in recommended_films:
                film_name = film.split(". ")[1].strip('"').strip("'")
                if (film_name not in res_names):
                    res_names.append(film_name)
            attempts += 1
            if attempts == 2:
                return "GigaChat can not respond to this request", 500

        return res_names

    except Exception as e:
        return {"error": str(e)}, 500
