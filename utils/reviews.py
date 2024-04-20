from flask import abort, jsonify, make_response
from sqlalchemy.exc import DBAPIError
from flask_jwt_extended import create_access_token

from configuration import db, encryptor
from entities import Review
from schemas import reviews_schema, review_schema

def get_review(username):
    try:
        review = Review.query.filter_by(username=username).one_or_none()
        if review is None:
            return abort(404, f"User with username '{username}' not found")

        return review_schema.dump(review), 200

    except DBAPIError as e:
        db.session.rollback()
        return {"error": str(e)}, 500

def post_review(username, body):
    try:
        existing_review = Review.query.filter_by(username=username).one_or_none()
        if existing_review is None:
            return abort(408, f"Invalid input or user with username '{username}' is not found.")

        new_review = Review(body)
        db.session.add(new_review)
        db.session.commit()

        return review_schema.dump(new_review), 201

    except DBAPIError as e:
        db.session.rollback()
        return {"error": str(e)}, 500

def delete_all_reviews(username):
    try:
        review = Review.query.filter_by(username=username).one_or_none()
        if review is None:
            return abort(404, f"User with username '{username}' not found")

        db.session.delete(review)
        db.session.commit()
        return f"All reviews of user with username '{username}' has been successfully deleted", 204

    except DBAPIError as e:
        db.session.rollback()
        return {"error": str(e)}, 500

def delete_review(id):
    try:
        review = Review.query.filter_by(id=id).one_or_none()
        if review is None:
            return abort(404, f"Review with id '{id}' not found")

        db.session.delete(review)
        db.session.commit()
        return f"Review with id '{id}' has been successfully deleted", 204

    except DBAPIError as e:
        db.session.rollback()
        return {"error": str(e)}, 500

def partial_update_review(id, body):
    try:
        review = Review.query.filter_by(id=id).one_or_none()
        if review is None:
            return abort(404, f"Review with id '{id}' not found")

        if 'viewed' in body:
            review.viewed = body['viewed']

        if 'review' in body:
            review.review = body['review']

        if 'reting' in body:
            review.reting = body['reting']

        db.session.commit()
        return review_schema.dump(review), 200

    except DBAPIError as e:
        db.session.rollback()
        return {"error": str(e)}, 500