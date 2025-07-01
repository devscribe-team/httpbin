# -*- coding: utf-8 -*-

"""
httpbin.api_routes
~~~~~~~~~~~~~~~~~~

Additional API routes for testing purposes.
"""

import random
import uuid
from datetime import datetime

from flask import Blueprint, jsonify, request

api_bp = Blueprint("api", __name__)


@api_bp.route("/api/users", methods=["GET"])
def list_users():
    """Returns a list of fake users.
    ---
    tags:
      - API Testing
    produces:
      - application/json
    responses:
      200:
        description: List of users.
    """
    users = [
        {"id": 1, "name": "John Doe", "email": "john@example.com", "active": True},
        {"id": 2, "name": "Jane Smith", "email": "jane@example.com", "active": False},
        {"id": 3, "name": "Bob Johnson", "email": "bob@example.com", "active": True},
    ]
    return jsonify({"users": users, "total": len(users)})


@api_bp.route("/api/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    """Returns a specific user by ID.
    ---
    tags:
      - API Testing
    parameters:
      - in: path
        name: user_id
        type: integer
    produces:
      - application/json
    responses:
      200:
        description: User details.
      404:
        description: User not found.
    """
    if user_id > 100:
        return jsonify({"error": "User not found"}), 404

    user = {
        "id": user_id,
        "name": f"User {user_id}",
        "email": f"user{user_id}@example.com",
        "created_at": "2023-01-01T00:00:00Z",
        "profile": {
            "bio": f"This is user {user_id}'s bio",
            "location": "Earth",
            "website": f"https://user{user_id}.example.com",
        },
    }
    return jsonify(user)


@api_bp.route("/api/users", methods=["POST"])
def create_user():
    """Creates a new user.
    ---
    tags:
      - API Testing
    consumes:
      - application/json
    produces:
      - application/json
    responses:
      201:
        description: User created successfully.
      400:
        description: Invalid input.
    """
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "Name is required"}), 400

    new_user = {
        "id": random.randint(1000, 9999),
        "name": data["name"],
        "email": data.get("email", ""),
        "created_at": datetime.utcnow().isoformat() + "Z",
        "active": True,
    }
    return jsonify(new_user), 201


@api_bp.route("/api/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    """Updates an existing user.
    ---
    tags:
      - API Testing
    parameters:
      - in: path
        name: user_id
        type: integer
    consumes:
      - application/json
    produces:
      - application/json
    responses:
      200:
        description: User updated successfully.
      404:
        description: User not found.
    """
    data = request.get_json()
    updated_user = {
        "id": user_id,
        "name": data.get("name", f"User {user_id}"),
        "email": data.get("email", f"user{user_id}@example.com"),
        "updated_at": datetime.utcnow().isoformat() + "Z",
    }
    return jsonify(updated_user)


@api_bp.route("/api/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    """Deletes a user.
    ---
    tags:
      - API Testing
    parameters:
      - in: path
        name: user_id
        type: integer
    responses:
      204:
        description: User deleted successfully.
      404:
        description: User not found.
    """
    return "", 204


@api_bp.route("/api/search", methods=["GET"])
def search():
    """Search endpoint with query parameters.
    ---
    tags:
      - API Testing
    parameters:
      - in: query
        name: q
        type: string
        required: true
      - in: query
        name: limit
        type: integer
        default: 10
      - in: query
        name: offset
        type: integer
        default: 0
    produces:
      - application/json
    responses:
      200:
        description: Search results.
    """
    query = request.args.get("q", "")
    limit = int(request.args.get("limit", 10))
    offset = int(request.args.get("offset", 0))

    # Generate fake search results
    results = []
    for i in range(min(limit, 20)):
        results.append(
            {
                "id": offset + i + 1,
                "title": f"Result {offset + i + 1} for '{query}'",
                "description": f"This is a fake search result containing '{query}'",
                "score": random.uniform(0.1, 1.0),
            }
        )

    return jsonify(
        {
            "query": query,
            "results": results,
            "total": random.randint(50, 1000),
            "limit": limit,
            "offset": offset,
        }
    )


@api_bp.route("/api/upload", methods=["POST"])
def upload_file():
    """File upload endpoint.
    ---
    tags:
      - API Testing
    consumes:
      - multipart/form-data
    produces:
      - application/json
    responses:
      200:
        description: File uploaded successfully.
    """
    files = request.files
    uploaded_files = []

    for key, file in files.items():
        uploaded_files.append(
            {
                "field_name": key,
                "filename": file.filename,
                "content_type": file.content_type,
                "size": len(file.read()),
                "upload_id": str(uuid.uuid4()),
            }
        )
        file.seek(0)  # Reset file pointer

    return jsonify(
        {
            "message": "Files uploaded successfully",
            "files": uploaded_files,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }
    )


@api_bp.route("/api/batch", methods=["POST"])
def batch_operation():
    """Batch operation endpoint.
    ---
    tags:
      - API Testing
    consumes:
      - application/json
    produces:
      - application/json
    responses:
      200:
        description: Batch operation completed.
    """
    data = request.get_json()
    operations = data.get("operations", [])

    results = []
    for i, op in enumerate(operations):
        results.append(
            {
                "operation_id": i,
                "type": op.get("type", "unknown"),
                "status": "success" if random.random() > 0.1 else "failed",
                "result": f"Operation {i} completed",
                "timestamp": datetime.utcnow().isoformat() + "Z",
            }
        )

    return jsonify(
        {
            "batch_id": str(uuid.uuid4()),
            "total_operations": len(operations),
            "results": results,
        }
    )


@api_bp.route("/api/webhook", methods=["POST"])
def webhook_receiver():
    """Webhook receiver endpoint.
    ---
    tags:
      - API Testing
    consumes:
      - application/json
    produces:
      - application/json
    responses:
      200:
        description: Webhook received successfully.
    """
    headers = dict(request.headers)
    data = request.get_json() if request.is_json else None

    return jsonify(
        {
            "message": "Webhook received",
            "received_at": datetime.utcnow().isoformat() + "Z",
            "headers": headers,
            "payload": data,
            "webhook_id": str(uuid.uuid4()),
        }
    )
