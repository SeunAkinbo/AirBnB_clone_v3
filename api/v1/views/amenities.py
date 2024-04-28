#!/usr/bin/python3
"""Amenities module"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', strict_slashes=False)
def get_amenities():
    """
    Retrieves the list of all Amenity objects.

    Returns:
        JSON: A list of all Amenity objects.
    """
    amenities = [amenity.to_dict() for amenity in
                 storage.all(Amenity).values()]
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False)
def get_amenity_by_id(amenity_id):
    """
    Retrieves an Amenity object by id.

    Args:
        amenity_id: The id of the Amenity object to retrieve

    Returns:
        JSON: The Amenity object if found, otherwise returns a 404 error.
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """
    Deletes an Amenity object by id.

    Args:
        amenity_id: The id of the Amenity object to delete.

    Returns:
        JSON: An empty dictionary with status code 200 if successful,
              otherwise returns a 404 error.
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Create an Amenity object

    Return:
        A new City object with the status code 201
    """
    if request.content_type != "application/json":
        abort(400, "Not a JSON")
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if "name" not in data:
        abort(400, "Missing name")
    new_amenity = Amenity(**data)
    new_amenity.save()
    return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Update an Amenity object

    Args:
        amenity_id: The id of the Amenity object to update

    Returns:
        JSON: The updated Amenity object
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if request.content_type != "application/json":
        abort(400, "Not a JSON")
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 200)
