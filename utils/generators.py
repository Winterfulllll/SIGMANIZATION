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
            content=f"Сгенерируй список из ровно {count} не повторяющихся IMDB ID значений фильмов, " +
            'рекомендованных данному пользователю. Ответ должен быть в формате JSON-списка.'
        )
        text = f"Предпочтения пользователя:\n"

        for preference in get_preference(username):
            text += f'- {preference["type"]}: {preference["type_value"]}\n'

        text += "\nОценки пользователя:\n"
        for review in get_review(username):
            rating = review.get("rating", None)
            if rating:
                film_response = requests.get(
                    url=f'ttps://api.kinopoisk.dev/v1.4/movie?externalId.imdb={review["item_id"]}&selectFields=name',
                    headers={'X-API-KEY': config["MOVIES_API"]}
                ).json()

                if film_response["total"] != 0:
                    text += f'''- "{film_response['docs']
                                    [0]['name']}": {rating},\n'''

        human_message = HumanMessage(content=text)
        response = giga([prompt, human_message])
        recommended_films = json.loads(response.content)

        attempts = 0
        while len(recommended_films) != count:
            human_message = HumanMessage(content=f"Сгенируй ровно {count} фильмов!\n" + text)
            response = giga([prompt, human_message])
            recommended_films = json.loads(response.content)
            attempts += 1
            if attempts == 2:
                return "GigaChat can not respond to this request", 500

        return recommended_films

    except Exception as e:
        return {"error": str(e)}, 500
