from flask import abort, jsonify, make_response
from sqlalchemy.exc import DBAPIError
from flask_jwt_extended import create_access_token
from datetime import timedelta

from configuration import db, encryptor
from entities import User
from schemas import users_schema, user_schema
from utils.validators import validate_username
from email_validator import validate_email


def get_all_users():
    """
    Returns a list of all users.
    """
    users = User.query.all()
    return users_schema.dump(users)


def register_user(body):
    """
    Creates a new user.

    Args:
        - body: Dictionary with user data (username, email, password, surname, name, patronymic).

    Returns:
        JSON representation of the created user and status code 201 on success
        or the corresponding error in case of failure.
    """
    try:
        username = body.get('username', None)
        email = body.get('email', None)
        password = body.get('password', None)
        surname = body.get('surname', None)
        name = body.get('name', None)
        patronymic = body.get('patronymic', None)

        if not all([username, email, password]):
            return jsonify(abort(400, "Missing required fields"))

        if not validate_username(body.get('username', None)):
            return jsonify(abort(400, f"Invalid username format"))

        try:
            validate_email(body.get('email', None))
        except:
            return abort(400, f"Invalid email format")

        existing_user = User.query.filter(
            (User.username == body.get('username', None)) | (
                User.email == body.get('email', None))
        ).one_or_none()

        if existing_user is not None:
            if existing_user.username == body.get('username', None):
                return abort(409, f"User with username '{body.get('username', None)}' already exists")
            else:
                return abort(409, f"User with email '{body.get('email', None)}' already exists")

        hashed_password = encryptor.encrypt_data(body.get('password', None))

        new_user = User(username=username, email=email,
                        password=hashed_password, surname=surname,
                        name=name, patronymic=patronymic)
        db.session.add(new_user)
        db.session.commit()

        return user_schema.dump(new_user), 201

    except DBAPIError as e:
        db.session.rollback()
        return {"error": str(e)}, 500


def delete_user(username):
    """
    Deletes a user by username.

    Args:
        - username: The username of the user to delete.

    Returns:
        JSON representation of the created user and status code 204 on success
        or the corresponding error in case of failure.
    """
    try:
        user = User.query.filter_by(username=username).one_or_none()
        if user is None:
            return abort(404, f"User with username '{username}' not found")

        db.session.delete(user)
        db.session.commit()
        return f"User with username '{username}' has been successfully deleted", 204

    except DBAPIError as e:
        db.session.rollback()
        return {"error": str(e)}, 500


def get_user(username):
    """
    Retrieves user information by username.

    Args:
        - username: The username of the user to delete.

    Returns:
        JSON representation of the created user and status code 200 on success
        or the corresponding error in case of failure.
    """
    try:
        user = User.query.filter_by(username=username).one_or_none()
        if user is None:
            return abort(404, f"User with username '{username}' not found")

        return user_schema.dump(user), 200

    except DBAPIError as e:
        db.session.rollback()
        return {"error": str(e)}, 500


def full_update_user(username, body):
    """
    Updates the user's settings, including the ability to change the username.

    Args:
        - username: The current user's username.
        - body: A dictionary with new user data.

    Returns:
        JSON representation of the created user and status code 200 on success
        or the corresponding error in case of failure.
    """
    try:
        new_username = body.get('username', None)
        new_email = body.get('email', None)
        new_password = body.get('password', None)
        new_surname = body.get('surname', None)
        new_name = body.get('name', None)
        new_patronymic = body.get('patronymic', None)

        user = User.query.filter_by(username=username).one_or_none()
        if user is None:
            return abort(404, f"User with username '{username}' not found")

        if not all([new_username, new_email, new_password]):
            return jsonify(abort(400, "Missing required fields"))

        if new_username != username:
            if User.query.filter_by(username=new_username).one_or_none() is not None:
                return abort(409, f"Username '{new_username}' already exists")
            if not validate_username(new_username):
                return abort(400, f"Invalid username format")
            user.username = new_username

        if new_email and new_email != user.email:
            try:
                validate_email(new_email)
            except:
                return abort(400, f"Invalid email format")

            if User.query.filter_by(email=new_email).one_or_none() is not None:
                return abort(409, f"Email '{new_email}' already exists")
            user.email = new_email

        hashed_password = encryptor.encrypt_data(new_password)
        user.password = hashed_password

        if new_surname:
            if (len(new_surname) > 50):
                return abort(400, f"Your surname is too long. The maximum length is 50")
            user.surname = new_surname

        if new_name:
            if (len(new_name) > 50):
                return abort(400, f"Your name is too long. The maximum length is 50")
            user.name = new_name

        if new_patronymic:
            if (len(new_patronymic) > 50):
                return abort(400, f"Your patronymic is too long. The maximum length is 50")
            user.patronymic = new_patronymic

        db.session.commit()
        return user_schema.dump(user), 200

    except DBAPIError as e:
        db.session.rollback()
        return {"error": str(e)}, 500


def partial_update_user(username, body):
    """
    Partially updates the user's settings.

    Args:
        - username: The current user's username.
        - body: A dictionary with new user data.

    Returns:
        JSON representation of the created user and status code 200 on success
        or the corresponding error in case of failure.
    """
    try:
        new_username = body.get('username', None)
        new_email = body.get('email', None)
        new_password = body.get('password', None)
        new_surname = body.get('surname', None)
        new_name = body.get('name', None)
        new_patronymic = body.get('patronymic', None)

        user = User.query.filter_by(username=username).one_or_none()
        if user is None:
            return abort(404, f"User with username '{username}' not found")

        if new_username and new_username != username:
            if User.query.filter_by(username=new_username).one_or_none() is not None:
                return abort(409, f"Username '{new_username}' already exists")
            if not validate_username(new_username):
                return abort(400, f"Invalid username format")
            user.username = new_username

        if new_email and new_email != user.email:
            try:
                validate_email(new_email)
            except:
                return abort(400, f"Invalid email format")

            if User.query.filter_by(email=new_email).one_or_none() is not None:
                return abort(409, f"Email '{new_email}' already exists")
            user.email = new_email

        if new_password:
            hashed_password = encryptor.encrypt_data(new_password)
            user.password = hashed_password

        if new_surname:
            if (len(new_surname) > 50):
                return abort(400, f"Your surname is too long. The maximum length is 50")
            user.surname = new_surname

        if new_name:
            if (len(new_name) > 50):
                return abort(400, f"Your name is too long. The maximum length is 50")
            user.name = new_name

        if new_patronymic:
            if (len(new_patronymic) > 50):
                return abort(400, f"Your patronymic is too long. The maximum length is 50")
            user.patronymic = new_patronymic

        db.session.commit()
        return user_schema.dump(user), 200

    except DBAPIError as e:
        db.session.rollback()
        return {"error": str(e)}, 500


def login(body):
    """
    Authenticates the user and returns the JWT token.

    Args:
        - body: Dictionary with user data (username, password, remember_me).

    Returns:
        JSON representation of the created user and status code 200 on success
        or the corresponding error in case of failure.
    """
    try:
        username = body.get('username', None)
        password = body.get('password', None)
        remember_me = body.get('remember_me', False)

        if not all([username, password, remember_me]):
            return jsonify(abort(400, "Missing required fields"))

        user = User.query.filter_by(username=username).one_or_none()
        if user is None:
            return abort(404, f"User with username '{username}' not found")

        if not encryptor.check_equivalence(password, user.password):
            return abort(401, "Invalid password")

        expires_delta = timedelta(days=30) if remember_me else None
        access_token = create_access_token(
            identity=username, expires_delta=expires_delta)

        response = make_response(jsonify(access_token=access_token), 200)
        response.set_cookie('access_token_cookie', access_token,
                            httponly=True, secure=True, samesite='Strict')
        return response

    except DBAPIError as e:
        return {"error": str(e)}, 500
