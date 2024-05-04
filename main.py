from flask import render_template
from configuration import connexion_app as app, app_config as config
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from utils.getters import get_movie_by_id


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
def movie_page(movie_id):
    try:
        verify_jwt_in_request()
        return render_template(
            'movie_page.html',
            movie=get_movie_by_id(movie_id),
            current_user_username=get_jwt_identity(),
            service_api_key=config["SECRET_KEY"]
        )

    except:
        return "Войдите в аккаунт!"


@app.route("/search")
def search():
    return render_template(
        'search.html',
        movies_api_key=config["MOVIES_API"]
    )

if __name__ == "__main__":
    app.run("main:app", host="0.0.0.0", port=8000)
