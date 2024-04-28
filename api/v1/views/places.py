#!/usr/bin/python3
"""User module"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def get_places(city_id):
    """
    Retrieves the list of all Place objects.
    
    Args:
        city_id: The id of the City to filter placess by

    Returns:
        JSON: A list of all Place objects.
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object by id.

    Args:
        place_id: The id of the Place object to retrieve

    Returns:
        JSON: The Place object if found, otherwise returns a 404 error.
    """
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict())
    abort(404)


@app_views.route("/places/<place_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object by id.

    Args:
        place_id: The id of the Place object to delete.

    Returns:
        JSON: An empty dictionary with status code 200 if successful,
        otherwise returns a 404 error.
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/cities/<city_id>/places", methods=["PUT"],
                 strict_slashes=False)
def create_place(city_id):
    """
    Creates a Place object linked to a City.

    Args:
        city_id: The id of the city to link the Place

    Return:
        JSON: The newly created Place object if successful,
        otherwise a 404 error
    """
    if request.content_type != "application/json":
        abort(400, "Not a JSON")
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if "user_id" not in data:
        abort(400, "Missing user_id")
    user = storage.get(User, data["user_id"])
    if not user:
        abort(404)
    if "name" not in data:
        abort(400, "Missing name")
    new_place = Place(**data)
    new_place.city_id = city_id
    new_place.save()
    return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], 
                 strict_slashes=True)
def update_place(place_id):
    """
    Updates a Place object by id.

    Args:
        place_id: The id of the Place object to update

    Returns:
        JSON: The updated Place object if successful,
        otherwise a 404 error
    """
    if request.content_type != "application/json":
        abort(400, "Not a JSON")
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at', 'user_id']:
            setattr(place, key, value)
    place.save()
    return make_response(jsonify(place.to_dict()), 200)