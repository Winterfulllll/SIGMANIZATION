from flask import abort
from sqlalchemy.exc import DBAPIError

from configuration import db
from entities import Review, User
from schemas import review_schema, reviews_schema


def get_review(username):
    reviews = Review.query.filter_by(username=username)
    return reviews_schema.dump(reviews)


def post_review(username, body):
    try:
        if not body.get('item_id', None) or not body.get('item_category', None) or not body.get('viewed', None):
            return abort(400, "Empty required fields")
        
        existing_user = User.query.filter_by(
            username=username).one_or_none()
        if existing_user is None:
            return abort(408, f"Invalid input or user with username '{username}' is not found.")
        
        existing_review = Review.query.filter_by(item_id=body.get('item_id')).one_or_none()
        if existing_review is not None:
            return abort(409, f"Review for item '{body.get('item_id')}' already exists")

        new_review = Review(username=username, item_id=body.get('item_id'), item_category=body.get('item_category'),
                            viewed=body.get('viewed'), review=body.get('review', None), rating=body.get('rating', None))
        db.session.add(new_review)
        db.session.commit()

        return review_schema.dump(new_review), 201

    except DBAPIError as e:
        db.session.rollback()
        return {"error": str(e)}, 500


def delete_all_reviews(username):
    try:
        user = Review.query.filter_by(username=username).first()
        if not user:
            return abort(404, f"User with username '{username}' not found")

        reviews = Review.query.filter_by(username=username).all()
        for review in reviews:
            db.session.delete(review)
        db.session.commit()
        return f"All reviews of user with username '{username}' has been successfully deleted", 204

    except DBAPIError as e:
        db.session.rollback()
        return {"error": str(e)}, 500


def delete_review(username, id):
    try:
        user = Review.query.filter_by(username=username).first()
        if not user:
            return abort(404, f"User with username '{username}' not found")
        
        review = Review.query.get(id)
        if not review:
            return abort(410, f"Review with id '{id}' not found")

        db.session.delete(review)
        db.session.commit()
        return f"Review with id '{id}' has been successfully deleted", 204

    except DBAPIError as e:
        db.session.rollback()
        return {"error": str(e)}, 500


def partial_update_review(username, id, body):
    try:
        user = Review.query.filter_by(username=username).first()
        if not user:
            return abort(404, f"User with username '{username}' not found")
        
        review = Review.query.filter_by(id=id).one_or_none()
        if review is None:
            return abort(404, f"Review with id '{id}' not found")

        if 'viewed' in body:
            review.viewed = body['viewed']

        if 'review' in body:
            review.review = body['review']

        if 'rating' in body:
            review.rating = body['rating']

        db.session.commit()
        return review_schema.dump(review), 200

    except DBAPIError as e:
        db.session.rollback()
        return {"error": str(e)}, 500
