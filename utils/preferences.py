from flask import abort
from sqlalchemy.exc import DBAPIError

from configuration import db
from entities import Preference, User
from schemas import preference_schema, preferences_schema


def get_preference(username):
    preferences = Preference.query.filter_by(username=username)
    return preferences_schema.dump(preferences)


def post_preference(username, body):
    try:
        existing_user = User.query.filter_by(
            username=username).one_or_none()
        if existing_user is None:
            return abort(408, f"Invalid input or user with username '{username}' is not found.")

        new_preference = Preference(username=username, type=body.get('type', None), category=body.get('category', None))
        db.session.add(new_preference)
        db.session.commit()

        return preference_schema.dump(new_preference), 201

    except DBAPIError as e:
        db.session.rollback()
        return {"error": str(e)}, 500


def delete_all_preferences(username):
    try:
        user = Preference.query.filter_by(username=username).first()
        if not user:
            return abort(404, f"User with username '{username}' not found")

        preferences = Preference.query.filter_by(username=username).all()
        for preference in preferences:
            db.session.delete(preference)
        db.session.commit()
        return f"All preferences of user with username '{username}' has been successfully deleted", 204

    except DBAPIError as e:
        db.session.rollback()
        return {"error": str(e)}, 500


def delete_preference(username, id):
    try:
        user = Preference.query.filter_by(username=username).first()
        if not user:
            return abort(404, f"User with username '{username}' not found")
        
        preference = Preference.query.get(id)
        if not preference:
            return abort(410, f"preference with id '{id}' not found")

        db.session.delete(preference)
        db.session.commit()
        return f"Preference with id '{id}' has been successfully deleted", 204

    except DBAPIError as e:
        db.session.rollback()
        return {"error": str(e)}, 500
