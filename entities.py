from configuration import db, app
from datetime import datetime, timezone
from marshmallow_enum import EnumField
from enum import Enum


class PreferenceType(Enum):
    GENRE = "genres.name"
    YEAR = "year"
    COUNTRY = "countries.name"
    RATING_IMDB = "rating.imdb"


class Category(Enum):
    MOVIES = "movies"
    BOOKS = "books"


class User(db.Model):
    __tablename__ = "users"
    username = db.Column(db.String(25), primary_key=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(255))
    surname = db.Column(db.String(50))
    name = db.Column(db.String(50))
    patronymic = db.Column(db.String(50))


class Preference(db.Model):
    __tablename__ = "preferences"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(25), db.ForeignKey('users.username'),
                         nullable=False)
    type = EnumField(PreferenceType, required=True)
    type_value = db.Column(db.Text)
    category = EnumField(Category, required=True)
    timestamp = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    user = db.relationship('User',
                           backref=db.backref('preferences', lazy=True))


class Review(db.Model):
    __tablename__ = "reviews"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(25), db.ForeignKey('users.username'),
                         nullable=False)
    item_id = db.Column(db.String(50), nullable=False)
    item_category = EnumField(Category, required=True)
    viewed = db.Column(db.Boolean, default=False)
    review = db.Column(db.Text)
    rating = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    user = db.relationship('User',
                           backref=db.backref('reviews', lazy=True))


with app.app_context():
    db.create_all()
