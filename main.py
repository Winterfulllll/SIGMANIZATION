from flask import render_template, abort
from configuration import connexion_app
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request


app = connexion_app
app.add_api("swagger.yml")


@app.route("/")
def home():
    try:
        verify_jwt_in_request()
        return render_template(
            "index.html",
            current_user_username=get_jwt_identity(),
            movies_api_key=app.app.config["MOVIES_API"]
        )

    except:
        return render_template(
            "index.html",
            movies_api_key=app.app.config["MOVIES_API"]
        )


@app.route("/profile")
def profile():
    try:
        verify_jwt_in_request()
        return render_template(
            "profile.html",
            current_user_username=get_jwt_identity()
        )

    except:
        return "Войдите в аккаунт!"


if __name__ == "__main__":
    app.run("main:app", host="0.0.0.0", port=8000)
