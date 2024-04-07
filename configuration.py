import os
import pathlib
import connexion
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from langchain.chat_models.gigachat import GigaChat

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
giga = GigaChat(credentials=os.getenv("GIGACHAT_AUTH"), verify_ssl_certs=False)
