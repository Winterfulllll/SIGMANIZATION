from utils import encryptor
from entities import User
from flask import abort
from jsonschema import ValidationError

from configuration import db, ma
from entities import User, users_schema, user_schema
from forms import UserForm
from utils import encryptor, validators


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
    form = UserForm(data=body)
    if form.validate():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        try:
            if not validators.validate_username(username):
                return abort(400, f"Invalid username format")

            if not validators.validate_email(email):
                return abort(400, f"Invalid email format")

            existing_user = User.query.filter(
                (User.username == username) | (User.email == email)
            ).one_or_none()

            if existing_user is not None:
                if existing_user.username == username:
                    return abort(409, f"User with username '{username}' already exists")
                else:
                    return abort(409, f"User with email '{email}' already exists")

            hashed_password = encryptor.encrypt_data(password)

            new_user = User(username=username, email=email,
                            password=hashed_password)
            db.session.add(new_user)
            db.session.commit()

            return user_schema.dump(new_user), 201

        except Exception:
            db.session.rollback()
            return {"error": "Internal Server Error"}, 500
    else:
        errors = {}
        for field, field_errors in form.errors.items():
            errors[field] = [str(error) for error in field_errors]
        return {"errors": errors}, 400


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

    except Exception:
        db.session.rollback()
        return {"error": "Internal Server Error"}, 500


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

    except Exception:
        return {"error": "Internal Server Error"}, 500


def update_user(current_username, body):
    """
    Обновляет параметры пользователя, включая возможность изменения username.

    Args:
        current_username: Текущее имя пользователя.
        body: Словарь с новыми данными пользователя.

    Returns:
        JSON-представление обновленного пользователя и код состояния 200 (OK) при успехе,
        или словарь с ошибкой и соответствующий код состояния при ошибке.
    """
    try:
        user = User.query.filter_by(username=current_username).one_or_none()
        if user is None:
            return abort(404, f"User with username '{current_username}' not found")

        new_username = body.get('username')
        if new_username and new_username != current_username:
            existing_user = User.query.filter_by(
                username=new_username).one_or_none()
            if existing_user is not None:
                return abort(409, f"Username '{new_username}' already exists")
            user.username = new_username

        new_email = body.get('email')
        if new_email and new_email != user.email:
            if not validators.validate_email(new_email):
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

    except Exception:
        db.session.rollback()
        return {"error": "Internal Server Error"}, 500
