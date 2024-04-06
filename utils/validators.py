import re

from email_validator import validate_email, EmailNotValidError


def validate_username(username):
    """
    Валидирует username:
    - Длина от 3 до 25 символов
    - Только буквы, цифры и подчеркивания
    - Не начинается и не заканчивается подчеркиванием
    """
    if not 3 <= len(username) <= 20:
        return False
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False
    if username.startswith('_') or username.endswith('_'):
        return False
    return True


def validate_email(email):
    """
    Валидирует email с использованием библиотеки email-validator.
    """
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False
