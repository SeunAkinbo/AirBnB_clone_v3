#!/usr/bin/python3
"""City Module"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def get_cities(state_id):
    """Retrieves the list of all City objects

    Args:
        state_id (str): State object ID

    Return:
        JSON City object, error 404 otherwise
    """
    states = storage.get(State, state_id)
    if not states:
        abort(404)
    cities = [city.to_dict() for city in states.cities]
    return jsonify(cities)


@app_views.route('/cities/<city_id>', strict_slashes=False)
def get_city_by_id(city_id):
    """Retrives the City object by its id

    Args:
        city_id (str): City object ID

    Return:
        JSON City object, error 404 otherwise
    """
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """Delete a City object by its id

    Args:
        city_id (str): City object ID
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """Create a City object

    Args:
        state_id (str): State object ID

    Return:
        A new City object with the status code 201
    """
    states = storage.get(State, state_id)
    if not states:
        abort(404)
    if request.content_type != "application/json":
        abort(400, "Not a JSON")
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if "name" not in data:
        abort(400, "Missing name")
    data["state_id"] = state_id
    city = City(**data)
    city.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """Update a City object

    Args:
        city_id (str): City object ID
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if request.content_type != "application/json":
        abort(400, "Not a JSON")
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at', 'state_id']:
            setattr(city, key, value)
    city.save()
    return make_response(jsonify(city.to_dict()), 200)
