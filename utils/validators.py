import re


def validate_username(username: str) -> bool:
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
