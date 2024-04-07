import os
import pathlib
import connexion
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from langchain.chat_models.gigachat import GigaChat
from utils.encryptor import Encryptor

base_dir = pathlib.Path(__file__).parent.resolve()
connexion_app = connexion.App(__name__, specification_dir=base_dir)

load_dotenv()
app = connexion_app.app

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + \
    str(base_dir / "data" / "reco.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['WTF_CSRF_ENABLED'] = False
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config["MOVIES_API"] = os.getenv("MOVIES_API")

db = SQLAlchemy(app)
ma = Marshmallow(app)
encryptor = Encryptor(os.getenv("FERNET_KEY"))
giga = GigaChat(credentials=os.getenv("GIGACHAT_AUTH"), verify_ssl_certs=False)
