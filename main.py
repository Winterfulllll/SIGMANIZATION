from flask import render_template
from configuration import connexion_app

app = connexion_app
app.add_api("swagger.yml")


@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run("main:app", host="0.0.0.0", port=8000)
