#!/usr/bin/python3
"""Place Module"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from models.state import State
from models.amenity import Amenity


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """Retrieves the list of all Place objects of a City

    Args:
        city_id (str): City object ID

    Return:
        JSON list of Place objects, error 404 otherwise
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place_by_id(place_id):
    """Retrieves a Place object by its id

    Args:
        place_id (str): Place object ID

    Return:
        JSON Place object, error 404 otherwise
    """
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict())
    abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Delete a Place object by its id

    Args:
        place_id (str): Place object ID
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Create a Place object

    Args:
        city_id (str): City object ID

    Return:
        A new Place object with the status code 201
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if request.content_type != "application/json":
        abort(400, "Not a JSON")
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if "user_id" not in data:
        abort(400, "Missing user_id")
    if "name" not in data:
        abort(400, "Missing name")
    user_id = data["user_id"]
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    data["city_id"] = city_id
    place = Place(**data)
    place.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """Update a Place object

    Args:
        place_id (str): Place object ID
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if request.content_type != "application/json":
        abort(400, "Not a JSON")
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    place.save()
    return make_response(jsonify(place.to_dict()), 200)


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def search_places():
    """Searches Place objects by filters

    Returns:
        JSON: List of Place objects matching filters, or error 40
    """
    if request.content_type != 'application/json':
        abort(400, 'Not a JSON')
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    states = data.get('states')
    cities = data.get('cities')
    amenities = data.get('amenities')
    if not (states or cities or amenities):
        places = storage.all(Place).values()
        list_places = [place.to_dict() for place in places]
        return jsonify(list_places)
    list_places = []

    if states:
        states_obj = [storage.get(State, state_id) for state_id in states]
        for state in states_obj:
            if state:
                for city in state.cities:
                    if city:
                        for place in city.places:
                            list_places.append(place)
    if cities:
        city_obj = [storage.get(City, city_id) for city_id in cities]
        for city in city_obj:
            if city:
                for place in city.places:
                    if place not in list_places:
                        list_places.append(place)
    if amenities:
        if not list_places:
            all_places = storage.all(Place).values()
            amenities_obj = [storage.get(Amenity, amenity_id)
                             for amenity_id in amenities]
            for place in all_places:
                if all([am in place.amenities for am in amenities_obj]):
                    list_places.append(place)
    places = []
    for plc_obj in list_places:
        plc_dict = plc_obj.to_dict()
        plc_dict.pop('amenities', None)
        places.append(plc_dict)
    return jsonify(places)
