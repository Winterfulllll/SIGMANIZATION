import connexion
import requests
from flask import render_template

app = connexion.App(__name__, specification_dir="./")
# app.add_api("swagger.yml")


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/profile")
def profile():
    return render_template("profile.html")

if __name__ == "__main__":
    app.run("main:app", host="0.0.0.0", port=8000) 
        