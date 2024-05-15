import os
import pathlib
import connexion

from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from langchain.chat_models.gigachat import GigaChat
from utils.encryptors import Encryptor
from flask_jwt_extended import JWTManager


load_dotenv()
base_dir = pathlib.Path(__file__).parent.resolve()
connexion_app = connexion.App(__name__, specification_dir=base_dir)
connexion_app.add_api("swagger.yml",
                      options={"swagger_ui": True,
                               "exclude_paths": ['/', '/<path:path>']})
app = connexion_app.app


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + \
    str(base_dir / "data" / "reco.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config["MOVIES_API"] = os.getenv("MOVIES_API")

app.config["JWT_TOKEN_LOCATION"] = ["cookies"]

app_config = app.config


def api_key_auth(token, required_scopes):
    if token != app_config['SECRET_KEY']:
        return
    return {"uid": "system"}


db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)
encryptor = Encryptor(os.getenv("FERNET_KEY"))
giga = GigaChat(credentials=os.getenv("GIGACHAT_AUTH"),
                verify_ssl_certs=False, model="GigaChat-Pro")
