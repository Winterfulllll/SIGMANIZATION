from configuration import db
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
    timestamp = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    user = db.relationship('User',
                           backref=db.backref('preferences', lazy=True))
