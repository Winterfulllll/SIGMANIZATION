import pathlib

import connexion
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

base_dir = pathlib.Path(__file__).parent.resolve()
connexion_app = connexion.App(__name__, specification_dir=base_dir)

load_dotenv()
app = connexion_app.app

app.config["MOVIES_API"] = os.getenv("MOVIES_API")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + \
    str(base_dir / "data" / "reco.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)
