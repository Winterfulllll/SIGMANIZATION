from flask import render_template
from configuration import connexion_app as app, app_config as config
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
import requests
import os

@app.route("/")
def home():
    try:
        verify_jwt_in_request()
        return render_template(
            "index.html",
            current_user_username=get_jwt_identity(),
            movies_api_key=config["MOVIES_API"],
            service_api_key=config["SECRET_KEY"]
        )

    except:
        return render_template(
            "index.html",
            movies_api_key=config["MOVIES_API"],
            service_api_key=config["SECRET_KEY"]
        )


@app.route("/profile")
def profile():
    try:
        verify_jwt_in_request()
        return render_template(
            "profile.html",
            current_user_username=get_jwt_identity(),
            service_api_key=config["SECRET_KEY"],
            movies_api_key=config["MOVIES_API"]
        )

    except:
        return "Войдите в аккаунт!"


@app.route("/settings")
def settings():
    try:
        verify_jwt_in_request()
        return render_template(
            "settings.html",
            current_user_username=get_jwt_identity()
        )

    except:
        return "Войдите в аккаунт!"

@app.route('/movie/<int:movie_id>')
def movie_detail(movie_id):
    # Запрашиваем данные о фильме из API
    try:
        film_response = requests.get(
            url = f'https://api.kinopoisk.dev/v1.4/movie?id={movie_id}&selectFields=id&selectFields=name&selectFields=description&selectFields=poster',
            headers={'X-API-KEY': os.getenv("MOVIES_API")}
        )



        movie = film_response.json()
        print(movie)
        return render_template('movie_detail.html', movie=movie)
    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == "__main__":
    app.run("main:app", host="0.0.0.0", port=8000)
