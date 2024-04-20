from flask import abort, jsonify, make_response
from sqlalchemy.exc import DBAPIError
from flask_jwt_extended import create_access_token

from configuration import db, encryptor
from entities import Preference
from schemas import preferences_schema, preference_schema

def get_preference(username):
    try:
        preference = Preference.query.filter_by(username=username).one_or_none()
        if preference is None:
            return abort(404, f"User with username '{username}' not found")

        return preference_schema.dump(preference), 200

    except DBAPIError as e:
        db.session.rollback()
        return {"error": str(e)}, 500

def post_preference(username, body):
    try:
        existing_preference = Preference.query.filter_by(username=username).one_or_none()
        if existing_preference is None:
            return abort(408, f"Invalid input or user with username '{username}' is not found.")

        new_preference = Preference(body)
        db.session.add(new_preference)
        db.session.commit()

        return preference_schema.dump(new_preference), 201

    except DBAPIError as e:
        db.session.rollback()
        return {"error": str(e)}, 500

def delete_all_preferences(username):
    try:
        preference = Preference.query.filter_by(username=username).one_or_none()
        if preference is None:
            return abort(404, f"User with username '{username}' not found")

        db.session.delete(preference)
        db.session.commit()
        return f"All preferences of user with username '{username}' has been successfully deleted", 204

    except DBAPIError as e:
        db.session.rollback()
        return {"error": str(e)}, 500

def delete_preference(id):
    try:
        preference = Preference.query.filter_by(id=id).one_or_none()
        if preference is None:
            return abort(404, f"Preference with id '{id}' not found")

        db.session.delete(preference)
        db.session.commit()
        return f"Preference with id '{id}' has been successfully deleted", 204

    except DBAPIError as e:
        db.session.rollback()
        return {"error": str(e)}, 500