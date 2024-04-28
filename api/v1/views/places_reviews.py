#!/usr/bin/python3
"""User module"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews', strict_slashes=False)
def get_reviews(place_id):
    """
    Retrieves the list of all Review objects.
    
    Args:
        place_id: The id of the Place to filter reviews by

    Returns:
        JSON: A list of all Review objects.
    """
    places = storage.get(Place, place_id)
    if not places:
        abort(404)
    reviews = [review.to_dict() for review in places.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', strict_slashes=False)
def get_review(review_id):
    """Retrieves a Review object by id.

    Args:
        review_id: The id of the Review object to retrieve

    Returns:
        JSON: The Review object if found, otherwise returns a 404 error.
    """
    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict())
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """
    Deletes a Review object by id.

    Args:
        review_id: The id of the Review object to delete.

    Returns:
        JSON: An empty dictionary with status code 200 if successful,
        otherwise returns a 404 error.
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
    """
    Creates a Review object.

    Args:
        place_id: The id of the Place associated with the review
    
    Return:
        JSON: The newly created Review object
    """
    if request.content_type != 'application/json':
        abort(400, 'Not a JSON')
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)
    if 'text' not in data:
        abort(400, 'Missing text')
    new_review = Review(**data)
    new_review.place_id = place.id
    new_review.save()
    return make_response(jsonify(new_review.to_dict(), 201))


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    if request.content_type != 'application/json':
        abort(400, 'Not a JSON')
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at', 'user_id']:
            setattr(review, key, value)
    review.save()
    return make_response(jsonify(review.to_dict()), 200)