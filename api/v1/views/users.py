#!/usr/bin/python3
"""User Module"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.users import User


@app_views.route('/users', strict_slashes=False)
def get_users():
    """
    Retrieves the list of all User objects.

    Returns:
        JSON: A list of all User objects.
    """
    users = [user.to_dict() for user in storage.all(User).values()]
    return jsonify(users)


@app_views.route('/users/<user_id>', strict_slashes=False)
def get_user_by_id(user_id):
    """Retrieves a User object by id.

    Args:
        user_id: The id of the User object to retrieve

    Returns:
        JSON: The User object if found, otherwise returns a 404 error.
    """
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """
    Deletes a User object by id.

    Args:
        user_id: The id of the User object to delete.

    Returns:
        JSON: An empty dictionary with status code 200 if successful,
              otherwise returns a 404 error.
    """
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def create_user():
    """
    Creates a User object.

    Returns:
        JSON: New User object with status code 201 if successful,
              otherwise returns a 400 error.
    """
    if request.content_type != "application/json":
        abort(400, "Not a JSON")
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if "email" not in data:
        abort(400, "Missing email")
    if "password" not in data:
        abort(400, "Missing password")
    new_user = User(**data)
    new_user.save()
    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """
    Updates a User object.

    Args:
        user_id (str): The ID of the User object to update.

    Returns:
        JSON: The updated User object with status code 200 if successful,
              otherwise returns a 404 error.
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if request.content_type != "application/json":
        return abort(400, "Not a JSON")
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(user, key, value)
    return make_response(jsonify(user.to_dict()), 200)
