from langchain.schema import HumanMessage, SystemMessage
from configuration import giga, app_config as config
from flask import jsonify
from utils.preferences import get_preference
from utils.reviews import get_review
import requests


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
        plot = response.content
        return plot

    except Exception as e:
        return jsonify({"error": f"Произошла непредвиденная ошибка: {str(e)}"}), 500


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
        films_header = {
            'X-API-KEY': config["MOVIES_API"]
        }

        prompt = SystemMessage(
            content="Ты - полезный помощник с искусственным интеллектом, обладающий обширными знаниями о фильмах. " +
            "Я предоставлю тебе какие фильмы нравятся пользователю и какие оценки он ставил различным фильмам. " +
            f"Ты на их основе сгенерируй список не повторяющихся IMDB ID рекомендованных данному пользователю фильмов, в количестве строго равном {count}. " +
            "Ответ должен быть в формате JSON списка")
        text = "Предпочтения пользователя:\n\n"

        for preference in get_preference(username):
            text += f'- {preference["type"]}:{preference["type_value"]}\n'

        text += "Оценки пользователя:\n\n"
        for review in get_review(username):
            film_response = requests.get(
                url=f'''https://api.kinopoisk.dev/v1.4/movie?externalId.imdb={review["item_id"]}&selectFields=name''',
                headers=films_header
            ).json()

            film_name = film_response["docs"]["name"]
            text += f'- {film_name}:{review["rating"]},\n'

        human_message = HumanMessage(content=text)
        response = giga([prompt, human_message])
        return jsonify(response.content)

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Ошибка при выполнении запроса: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Произошла непредвиденная ошибка: {str(e)}"}), 500
