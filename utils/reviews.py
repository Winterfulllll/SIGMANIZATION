from flask import abort
from sqlalchemy.exc import DBAPIError

from configuration import db
from entities import Review, User
from schemas import review_schema, reviews_schema


def get_review(username):
    """
    Returns all user reviews by username.
    """
    reviews = Review.query.filter_by(username=username)
    return reviews_schema.dump(reviews)


def post_review(username, body):
    """
    Creates a new user review.

    Args:
        - username: The user's name.
        - body: A dictionary with user review data (item_id, item_category, viewed, rating, review).

    Returns:
        JSON representation of the created review and status code 201 on success
        or the corresponding error in case of failure.
    """
    try:
        item_id = body.get('item_id', None)
        item_category = body.get('item_category', None)
        viewed = body.get('viewed', None)
        review = body.get('review', None)
        rating = body.get('rating', None)

        if not all([item_id, item_category, viewed]):
            return abort(400, "Empty required fields")

        if User.query.filter_by(username=username).one_or_none() is None:
            return abort(408, f"Invalid input or user with username '{username}' is not found.")

        if Review.query.filter((Review.username == username) & (Review.item_id == item_id) & (
            Review.item_category == item_category)).one_or_none() is not None:
            return abort(409, f"Review for item '{body.get('item_id')}' already exists")

        new_review = Review(username=username, item_id=item_id, item_category=item_category,
                            viewed=viewed, review=review, rating=rating)
        db.session.add(new_review)
        db.session.commit()

        return review_schema.dump(new_review), 201

    except DBAPIError as e:
        db.session.rollback()
        return {"error": str(e)}, 500


def delete_all_reviews(username):
    """
    Deletes all user reviews by name.

    Args:
        - username: The current user's name.

    Returns:
        Successful deletion message and status code 204
        or the corresponding error in case of failure.
    """
    try:
        if not Review.query.filter_by(username=username).first():
            return abort(404, f"User with username '{username}' not found")

        reviews = Review.query.filter_by(username=username).all()
        for review in reviews:
            db.session.delete(review)
        db.session.commit()
        return "All reviews of user with username '{username}' has been successfully deleted", 204

    except DBAPIError as e:
        db.session.rollback()
        return {"error": str(e)}, 500


def delete_review(id):
    """
    Deletes the user's review by the review id.

    Args:
        - id: The ID of the review to delete.

    Returns:
        Successful deletion message and status code 204
        or the corresponding error in case of failure.
    """
    try:
        review = Review.query.filter_by(id=id).one_or_none()
        if not review:
            return abort(410, f"Review with id '{id}' not found")

        db.session.delete(review)
        db.session.commit()
        return "Review with id '{id}' has been successfully deleted", 204

    except DBAPIError as e:
        db.session.rollback()
        return {"error": str(e)}, 500


def partial_update_review(id, body):
    """
    Partially updates the user's review parameters.

    Args:
        - id: The ID of the review to update.
        - body: Dictionary with data to update.

    Returns:
        JSON representation of the updated review and status code 200 on success
        or the corresponding error in case of failure.
    """
    try:
        viewed = body.get('viewed', None)
        review = body.get('review', None)
        rating = body.get('rating', None)

        review_object = Review.query.filter_by(id=id).one_or_none()
        if review_object is None:
            return abort(404, f"Review with id '{id}' not found")

        if viewed:
            review_object.viewed = viewed

        if review:
            review_object.review = review

        if rating:
            review_object.rating = rating

        db.session.commit()
        return review_schema.dump(review_object), 200

    except DBAPIError as e:
        db.session.rollback()
        return {"error": str(e)}, 500
