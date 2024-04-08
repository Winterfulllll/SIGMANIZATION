from flask import request, jsonify
from entities import User
from utils.validators import validate_username
from email_validator import validate_email

def check_username():
    username = request.args.get('username')
    if not validate_username(username):
        return jsonify({'error': 'Invalid username format'}), 400

    try:
        user = User.query.filter(User.username == username).one_or_none()
        return jsonify({'exists': user is not None})
    except Exception:
        return jsonify({'error': 'Internal Server Error'}), 500


def check_email():
    email = request.args.get('email')
    if not validate_email(email):
        return jsonify({'error': 'Invalid email format'}), 400

    try:
        user = User.query.filter(User.email == email).one_or_none()
        return jsonify({'exists': user is not None})
    except Exception:
        return jsonify({'error': 'Internal Server Error'}), 500
