#!/usr/bin/python3
"""State module"""
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """
    Retrieves the list of all State objects.

    Returns:
        JSON: A list of all State objects.
    """
    states = [state.to_dict() for state in storage.all(State).values()]
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """
    Retrieves a State object.

    Args:
        state_id (str): The ID of the State object to retrieve.

    Returns:
        JSON: The State object if found, otherwise returns a 404 error.
    """
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    else:
        abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """
    Deletes a State object.

    Args:
        state_id (str): The ID of the State object to delete.

    Returns:
        JSON: An empty dictionary with status code 200 if successful,
              otherwise returns a 404 error.
    """
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """
    Creates a State object.

    Returns:
        JSON: New State object with status code 201 if successful,
              otherwise returns a 400 error.
    """
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if "name" not in data:
        abort(400, "Missing name")
    new_state = State(**data)
    new_state.save()
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def update_state(state_id):
    """
    Updates a State object.

    Args:
        state_id (str): The ID of the State object to update.

    Returns:
        JSON: The updated State object with status code 200 if successful,
              otherwise returns a 404 error.
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
