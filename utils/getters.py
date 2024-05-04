from configuration import app_config as config
import requests


def get_film(movie_id):
    film_response = requests.get(
        url=f'https://api.kinopoisk.dev/v1.4/movie?externalId.imdb={movie_id}&selectFields=name,description,poster.url',
        headers={'X-API-KEY': config["MOVIES_API"]}
    )
    return film_response.json()
