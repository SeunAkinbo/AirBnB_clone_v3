#!/usr/bin/python3
"""Places Reviews Module"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """Retrieves the list of all Review objects of a Place

    Args:
        place_id (str): Place object ID

    Return:
        JSON list of Review objects, error 404 otherwise
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review_by_id(review_id):
    """Retrieves a Review object by its id

    Args:
        review_id (str): Review object ID

    Return:
        JSON Review object, error 404 otherwise
    """
    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict())
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Delete a Review object by its id

    Args:
        review_id (str): Review object ID
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """Create a Review object

    Args:
        place_id (str): Place object ID

    Return:
        A new Review object with the status code 201
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if request.content_type != "application/json":
        abort(400, "Not a JSON")
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if "user_id" not in data:
        abort(400, "Missing user_id")
    if "text" not in data:
        abort(400, "Missing text")
    user_id = data["user_id"]
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    data["place_id"] = place_id
    review = Review(**data)
    review.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """Update a Review object

    Args:
        review_id (str): Review object ID
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    if request.content_type != "application/json":
        abort(400, "Not a JSON")
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    keys_to_ignore = ['id', 'user_id', 'place_id', 'created_at',
                      'updated_at']
    for key, value in data.items():
        if key not in keys_to_ignore:
            setattr(review, key, value)
    review.save()
    return make_response(jsonify(review.to_dict()), 200)
