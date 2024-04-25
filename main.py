from flask import render_template
from configuration import connexion_app
from flask_jwt_extended import get_jwt_identity, jwt_required


app = connexion_app
app.add_api("swagger.yml")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/profile")
@jwt_required()
def profile():
    return render_template("profile.html", current_user_username=get_jwt_identity())


@app.route("/settings")
def settings():
    return render_template("settings.html")


if __name__ == "__main__":
    app.run("main:app", host="0.0.0.0", port=8000)
