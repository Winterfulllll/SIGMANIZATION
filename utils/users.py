from flask import abort, jsonify, make_response
from sqlalchemy.exc import DBAPIError
from flask_jwt_extended import create_access_token
from datetime import timedelta

from configuration import db
from entities import User
from schemas import users_schema, user_schema
from utils.validators import validate_username
from utils.hashing import hash_string, check_equivalence
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

        if not validate_username(username):
            return jsonify(abort(400, f"Invalid username format"))

        try:
            validate_email(email)
        except:
            return abort(400, f"Invalid email format")

        existing_user = User.query.filter(
            (User.username == username) | (User.email == email)).one_or_none()

        if existing_user is not None:
            if existing_user.username == username:
                return abort(409, f"User with username '{username}' already exists")
            else:
                return abort(409, f"User with email '{email}' already exists")

        hashed_password = hash_string(password)

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
    Updates the user's settings, including the ability to change the user name.

    Arguments:
        - username: The current username.
        - body: Dictionary with new user data.

    Returns:
        JSON representation of an updated user with a new JWT token
        and the status code 200 in case of success,
        or an appropriate error in case of failure.
    """
    try:
        new_username = body.get('username', None)
        new_email = body.get('email', None)
        new_password = body.get('password', None)
        new_surname = body.get('surname', None)
        new_name = body.get('name', None)
        new_patronymic = body.get('patronymic', None)
        access_token = None

        user = User.query.filter_by(username=username).one_or_none()
        if user is None:
            return abort(404, f"Пользователь с именем '{username}' не найден")

        if not all([new_username, new_email, new_password]):
            return jsonify(abort(400, "Отсутствуют обязательные поля"))

        if new_username != username:
            if User.query.filter_by(username=new_username).one_or_none() is not None:
                return abort(409, f"Имя пользователя '{new_username}' уже существует")
            if not validate_username(new_username):
                return abort(400, f"Неверный формат имени пользователя")
            user.username = new_username

            access_token = create_access_token(
                identity=new_username, expires_delta=timedelta(days=30))

        if new_email and new_email != user.email:
            try:
                validate_email(new_email)
            except:
                return abort(400, f"Неверный формат email")

            if User.query.filter_by(email=new_email).one_or_none() is not None:
                return abort(409, f"Email '{new_email}' уже используется")
            user.email = new_email

        hashed_password = hash_string(new_password)
        user.password = hashed_password

        if new_surname:
            if len(new_surname) > 50:
                return abort(400, f"Фамилия слишком длинная. Максимальная длина - 50 символов")
            user.surname = new_surname

        if new_name:
            if len(new_name) > 50:
                return abort(400, f"Имя слишком длинное. Максимальная длина - 50 символов")
            user.name = new_name

        if new_patronymic:
            if len(new_patronymic) > 50:
                return abort(400, f"Отчество слишком длинное. Максимальная длина - 50 символов")
            user.patronymic = new_patronymic

        db.session.commit()

        if not access_token:
            access_token = create_access_token(identity=username, fresh=True)

        response = make_response(jsonify(access_token=access_token), 200)
        response.set_cookie('access_token_cookie', access_token,
                            httponly=True, secure=True, samesite='Strict')
        return response

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
            hashed_password = hash_string(new_password)
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
        remember_me = body.get('remember_me', None)

        if not all([username, password, remember_me is not None]):
            return jsonify(abort(400, "Missing required fields"))

        user = User.query.filter_by(username=username).one_or_none()
        if user is None:
            return abort(404, f"User with username '{username}' not found")

        if not check_equivalence(password, user.password):
            return abort(401, "Invalid password")

        if remember_me:
            access_token = create_access_token(
                identity=username, expires_delta=timedelta(days=30))
        else:
            access_token = create_access_token(identity=username, fresh=True)

        response = make_response(jsonify(access_token=access_token), 200)
        response.set_cookie('access_token_cookie', access_token,
                            httponly=True, secure=True, samesite='Strict')
        return response

    except DBAPIError as e:
        return {"error": str(e)}, 500


def password_check(body) -> bool:
    try:
        username = body.get('username', None)
        password = body.get('password', None)
        user = User.query.filter_by(username=username).one_or_none()

        if not all([username, password]):
            return abort(400, "Missing required fields")

        if user is None:
            return abort(404, f"User with username '{username}' not found")

        return check_equivalence(password, user.password)

    except DBAPIError as e:
        return {"error": str(e)}, 500


def logout():
    """
    Logs out the user by clearing the JWT cookie.

    Returns:
        A message indicating successful logout and status code 200.
    """
    response = make_response(
        jsonify({"message": "Logged out successfully"}), 200)
    response.set_cookie('access_token_cookie', '', expires=0)
    return response
