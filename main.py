from flask import render_template
from configuration import connexion_app
from flask_jwt_extended import jwt_required, get_jwt_identity


app = connexion_app
app.add_api("swagger.yml")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/profile")
@jwt_required()
def profile():
    current_user = get_jwt_identity()
    return render_template("profile.html")


if __name__ == "__main__":
    app.run("main:app", host="0.0.0.0", port=8000)
