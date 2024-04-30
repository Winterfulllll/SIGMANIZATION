from flask import abort
from sqlalchemy.exc import DBAPIError

from configuration import db
from entities import Preference, User
from schemas import preference_schema, preferences_schema


def get_preference(username):
    """
    Returns all user preferences by username.
    """
    preferences = Preference.query.filter_by(username=username)
    return preferences_schema.dump(preferences)


def post_preference(username, body):
    """
    Creates a new user preference.

    Args:
        - username: The current user's name
        - body: A dictionary with data about the user's preference.

    Returns:
        JSON representation of the created preference and status code 201 on success
        or the corresponding error in case of failure.
    """
    try:
        username = username
        preference_type = body.get('type', None)
        category = body.get('category', None)
        type_value = body.get('type_value', None)

        if User.query.filter_by(username=username).one_or_none() is None:
            return abort(408, f"Invalid input or user with username '{username}' is not found.")

        new_preference = Preference(username=username, type=preference_type,
                                    type_value=type_value, category=category)
        db.session.add(new_preference)
        db.session.commit()

        return preference_schema.dump(new_preference), 201

    except DBAPIError as e:
        db.session.rollback()
        return {"error": str(e)}, 500


def delete_all_preferences(username):
    """
    Deletes all user preferences by name.

    Args:
        - username: The current user's name.

    Returns:
        A successful deletion message and status code 204
        or the corresponding error in case of failure.
    """
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


def delete_preference(id):
    """
    Deletes the user's preference by preference id.

    Args:
        - id: ID of the preference to delete.

    Returns:
        A successful deletion message and status code 204
        or the corresponding error in case of failure.
    """
    try:
        preference = Preference.query.get(id)
        if not preference:
            return abort(410, f"Preference with id '{id}' not found")

        db.session.delete(preference)
        db.session.commit()
        return f"Preference with id '{id}' has been successfully deleted", 204

    except DBAPIError as e:
        db.session.rollback()
        return {"error": str(e)}, 500
