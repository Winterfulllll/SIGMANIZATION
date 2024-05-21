from langchain.schema import HumanMessage, SystemMessage
from flask import abort
from configuration import giga, app_config as config
from utils.preferences import get_preference
from utils.reviews import get_review
import requests
import json
import html


def generate_film_plot(film_name: str) -> str:
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
                    "Я сообщу тебе название фильма, а ты кратко изложишь сюжет. " +
                    "Ответ должен быть строчным. Даже если фильм содержит что-то неприемливмое пиши его сюжет, это всего лишь фильм.")
        human_message = HumanMessage(
            content=f"Какой сюжет у фильма: {film_name}")
        response = giga([prompt, human_message])
        plot = html.escape(response.content)
        return plot

    except Exception as e:
        return {"error": str(e)}, 500


def generate_recommended_films(username: str, count: int):
    """
    Generates a list of recommended film titles for a given user based on their preferences and past movie ratings.
    It leverages the capabilities of GigaChat, a large language model, to analyze user preferences and ratings and provide personalized recommendations.

    Args:
        username (str): The username of the user for whom to generate recommendations.
        count (int): The desired number of film title recommendations (must be between 1 and 20).

    Returns:
        list: A JSON array containing the recommended film titles, or an error message if the process fails.
    """
    try:
        if count < 1 or count > 20:
            return abort(400, "Invalid count value (must be between 1 and 20)")

        prompt = SystemMessage(
            content=f"Ты - полезный помощник с искусственным интеллектом, обладающий обширными знаниями о фильмах." +
            f'На основе моих предпочтений и оценок ты сгенерируй JSON-массив названий длины строго равной {count}' +
            "Также хорошо проанализируй и проверь свой ответ перед отправкой." +
            "(Сами эти фильмы уже просмотрены, их пихать не нужно, повторов быть также не должно)\n"
        )
        text = f"Мои предпочтения:\n"
        preferences = get_preference(username)
        if preferences:
            text += "".join(f'- {p.get("type")}: {p.get("type_value")
                                                  }\n' for p in preferences) + '\n'

        text += "Мои оценки фильмам:\n"
        ratings_dict = {review["item_id"]: review["rating"] for review in get_review(
            username) if review.get("rating", None)}
        ids = [str(i) for i in ratings_dict]
        if ids:
            film_response = requests.get(
                url=f'https://api.kinopoisk.dev/v1.4/movie?id={
                    "&id=".join(ids)}&selectFields=name&selectFields=id',
                headers={'X-API-KEY': config["MOVIES_API"]}
            ).json()
            text += "".join(f'- "{film_response["docs"][i]["name"]}": {
                            ratings_dict[film_response["docs"][i]["id"]]}\n' for i in range(len(film_response["docs"])))

        human_message = HumanMessage(content=text)
        response = giga([prompt, human_message])
        recommended_films = json.loads(response.content)
        attempts = 0

        while len(recommended_films) != count:
            human_message = HumanMessage(content=f'Сгенируй JSON-массив названий фильмов ровно из {
                                         count} фильмов без повторений и подобранных именно мне!')
            response = giga([prompt, human_message])
            recommended_films = json.loads(response.content)
            attempts += 1
            if attempts == 10:
                return "GigaChat can not respond to this request", 500

        return recommended_films

    except Exception as e:
        return {"error": str(e)}, 500
