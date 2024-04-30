import re


def validate_username(username: str) -> bool:
    """
    Validates the username by:
        - Length from 3 to 25 characters
        - Only letters, numbers and underscores
        - Does not begin or end with an underscore
    """
    if not 3 <= len(username) <= 25:
        return False
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False
    if username.startswith('_') or username.endswith('_'):
        return False
    return True
