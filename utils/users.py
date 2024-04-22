from flask import abort, jsonify, make_response
from sqlalchemy.exc import DBAPIError
from flask_jwt_extended import create_access_token

from configuration import db, encryptor
from entities import User
from schemas import users_schema, user_schema
from utils.validators import validate_username
from email_validator import validate_email


def get_all_users():
    """
    Возвращает список всех пользователей
    """
    users = User.query.all()
    return users_schema.dump(users)


def register_user(body):
    """
    Создает нового пользователя.

    Args:
        body: Словарь с данными пользователя (username, email, password).

    Returns:
        JSON-представление созданного пользователя и код состояния 201 при успехе,
        или словарь с ошибками и соответствующий код состояния при ошибке.
    """
    try:
        if not all(key in body for key in ("username", "email", "password")):
            return abort(400, "Missing required fields")

        if not body.get('username', None) or not body.get('email', None) or not body.get('password', None):
            return abort(400, "Empty required fields")
        if not validate_username(body.get('username', None)):
            return abort(400, f"Invalid username format")

        if not validate_email(body.get('email', None)):
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

        new_user = User(username=body.get('username', None), email=body.get('email', None),
                        password=hashed_password, surname=body.get(
                            'surname', None),
                        name=body.get('name', None), patronymic=body.get('patronymic', None))
        db.session.add(new_user)
        db.session.commit()

        return user_schema.dump(new_user), 201

    except DBAPIError as e:
        db.session.rollback()
        return {"error": str(e)}, 500


def delete_user(username):
    """
    Удаляет пользователя по имени пользователя.

    Args:
        username: Имя пользователя для удаления.

    Returns:
        Сообщение об успешном удалении и код состояния 204 (No Content),
        или словарь с ошибкой и соответствующий код состояния.
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
    Получает информацию о пользователе по имени пользователя.

    Args:
        username: Имя пользователя.

    Returns:
        JSON-представление пользователя и код состояния 200 (OK),
        или словарь с ошибкой и соответствующий код состояния.
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
    Обновляет параметры пользователя, включая возможность изменения username.

    Args:
        username: Текущее имя пользователя.
        body: Словарь с новыми данными пользователя.

    Returns:
        JSON-представление обновленного пользователя и код состояния 200 (OK) при успехе,
        или словарь с ошибкой и соответствующий код состояния при ошибке.
    """
    try:
        user = User.query.filter_by(username=username).one_or_none()
        if user is None:
            return abort(404, f"User with username '{username}' not found")

        new_username = body.get('username')
        if new_username and new_username != username:
            existing_user = User.query.filter_by(
                username=new_username).one_or_none()
            if existing_user is not None:
                return abort(409, f"Username '{new_username}' already exists")
            user.username = new_username

        new_email = body.get('email')
        if new_email and new_email != user.email:
            if not validate_email(new_email):
                return abort(400, "Invalid email format")
            existing_user = User.query.filter_by(email=new_email).one_or_none()
            if existing_user is not None:
                return abort(409, f"Email '{new_email}' already exists")
            user.email = new_email

        if 'password' in body:
            hashed_password = encryptor.encrypt_data(body['password'])
            user.password = hashed_password
        if 'surname' in body:
            user.surname = body['surname']
        if 'name' in body:
            user.name = body['name']
        if 'patronymic' in body:
            user.patronymic = body['patronymic']

        db.session.commit()
        return user_schema.dump(user), 200

    except DBAPIError as e:
        db.session.rollback()
        return {"error": str(e)}, 500


def partial_update_user(username, body):
    """
    Частично обновляет параметры пользователя.

    Args:
        username: Имя пользователя.
        body: Словарь с данными для обновления.

    Returns:
        JSON-представление обновленного пользователя и код состояния 200 (OK) при успехе,
        или словарь с ошибкой и соответствующий код состояния при ошибке.
    """
    try:
        user = User.query.filter_by(username=username).one_or_none()
        if user is None:
            return abort(404, f"User with username '{username}' not found")

        if 'email' in body:
            new_email = body['email']
            if new_email != user.email:
                if not validate_email(new_email):
                    return abort(400, "Invalid email format")
                existing_user = User.query.filter_by(
                    email=new_email).one_or_none()
                if existing_user is not None:
                    return abort(409, f"Email '{new_email}' already exists")
                user.email = new_email

        if 'password' in body:
            hashed_password = encryptor.encrypt_data(body['password'])
            user.password = hashed_password

        if 'surname' in body:
            user.surname = body['surname']

        if 'name' in body:
            user.name = body['name']

        if 'patronymic' in body:
            user.patronymic = body['patronymic']

        db.session.commit()
        return user_schema.dump(user), 200

    except DBAPIError as e:
        db.session.rollback()
        return {"error": str(e)}, 500


def login(body):
    """
    Аутентифицирует пользователя и возвращает JWT-токен.

    Args:
        body: Словарь с данными пользователя (username, password, remember_me).

    Returns:
        JSON-объект с JWT-токеном и кодом состояния 200 при успехе,
        или словарь с ошибкой и соответствующий код состояния при ошибке.
    """
    try:
        username = body.get('username', None)
        password = body.get('password', None)
        remember_me = body.get('remember_me', False)

        user = User.query.filter_by(username=username).one_or_none()
        if user is None:
            return abort(404, f"User with username '{username}' not found")

        if not encryptor.check_equivalence(password, user.password):
            return abort(401, "Invalid password")

        access_token = create_access_token(
            identity=username, expires_delta=False if remember_me else None)

        response = make_response(jsonify(access_token=access_token), 200)
        response.set_cookie('jwt_token', access_token,
                            httponly=True, secure=True)
        return response

    except DBAPIError as e:
        return {"error": str(e)}, 500
