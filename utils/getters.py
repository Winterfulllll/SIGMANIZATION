from utils.generators import generate_film_plot
from configuration import app_config as config
import requests


def get_movie_info_by_id(movie_id):
    movie_response = requests.get(
        url=f'https://api.kinopoisk.dev/v1.4/movie?id={
            movie_id}&selectFields=id&selectFields=name&selectFields=poster',
        headers={'X-API-KEY': config["MOVIES_API"]}
    ).json()
    movie_response["docs"][0]["description"] = generate_film_plot(
        movie_response["docs"][0]["name"])
    return movie_response
