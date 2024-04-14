from configuration import db, app
from datetime import datetime, timezone


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
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(25), db.ForeignKey('users.username'),
                        nullable=False)
    preference = db.Column(db.Text, nullable=False)
    # Тип в рамках Kinopoisk API: "genre", "year" и т.т.
    type = db.Column(db.String(50), nullable=False)
    # Категория: "film", "book" и т.п.
    category = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    user = db.relationship('User',
                           backref=db.backref('preferences', lazy=True))


class Review(db.Model):
    __tablename__ = "reviews"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(25), db.ForeignKey('users.username'),
                        nullable=False)
    item_id = db.Column(db.Integer, nullable=False)
    item_type = db.Column(db.String(50), nullable=False)
    review = db.Column(db.Text)
    rating = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    user = db.relationship('User',
                           backref=db.backref('reviews', lazy=True))


with app.app_context():
    db.create_all()
