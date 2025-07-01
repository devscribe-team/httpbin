# -*- coding: utf-8 -*-

"""
httpbin.advanced_routes
~~~~~~~~~~~~~~~~~~~~~~~

Advanced API routes for complex testing scenarios.
"""

import csv
import io
import json
import random
import time
from datetime import datetime

from flask import Blueprint, Response, jsonify, request

advanced_bp = Blueprint("advanced", __name__)


@advanced_bp.route("/advanced/streaming", methods=["GET"])
def streaming_response():
    """Returns a streaming response with multiple chunks.
    ---
    tags:
      - Advanced
    parameters:
      - in: query
        name: chunks
        type: integer
        default: 10
      - in: query
        name: delay
        type: number
        default: 0.5
    produces:
      - application/json
    responses:
      200:
        description: Streaming response.
    """
    chunks = min(int(request.args.get("chunks", 10)), 100)
    delay = min(float(request.args.get("delay", 0.5)), 5.0)

    def generate():
        for i in range(chunks):
            chunk_data = {
                "chunk": i + 1,
                "total_chunks": chunks,
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "data": f"This is chunk {i + 1} of {chunks}",
            }
            yield json.dumps(chunk_data) + "\n"
            if i < chunks - 1:  # Don't delay after last chunk
                time.sleep(delay)

    return Response(generate(), mimetype="application/json")


@advanced_bp.route("/advanced/paginated", methods=["GET"])
def paginated_data():
    """Returns paginated data with navigation links.
    ---
    tags:
      - Advanced
    parameters:
      - in: query
        name: page
        type: integer
        default: 1
      - in: query
        name: per_page
        type: integer
        default: 20
      - in: query
        name: total_items
        type: integer
        default: 1000
    produces:
      - application/json
    responses:
      200:
        description: Paginated response.
    """
    page = max(1, int(request.args.get("page", 1)))
    per_page = min(max(1, int(request.args.get("per_page", 20))), 100)
    total_items = int(request.args.get("total_items", 1000))

    total_pages = (total_items + per_page - 1) // per_page
    start_idx = (page - 1) * per_page
    end_idx = min(start_idx + per_page, total_items)

    items = []
    for i in range(start_idx, end_idx):
        items.append(
            {
                "id": i + 1,
                "name": f"Item {i + 1}",
                "value": random.randint(1, 1000),
                "category": random.choice(["A", "B", "C"]),
            }
        )

    base_url = request.base_url

    pagination = {
        "page": page,
        "per_page": per_page,
        "total_items": total_items,
        "total_pages": total_pages,
        "has_prev": page > 1,
        "has_next": page < total_pages,
        "prev_page": page - 1 if page > 1 else None,
        "next_page": page + 1 if page < total_pages else None,
        "links": {
            "first": f"{base_url}?page=1&per_page={per_page}",
            "last": f"{base_url}?page={total_pages}&per_page={per_page}",
            "prev": f"{base_url}?page={page - 1}&per_page={per_page}"
            if page > 1
            else None,
            "next": f"{base_url}?page={page + 1}&per_page={per_page}"
            if page < total_pages
            else None,
        },
    }

    return jsonify(
        {
            "items": items,
            "pagination": pagination,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }
    )


@advanced_bp.route("/advanced/graphql", methods=["POST"])
def graphql_simulator():
    """Simulates a GraphQL endpoint.
    ---
    tags:
      - Advanced
    consumes:
      - application/json
    produces:
      - application/json
    responses:
      200:
        description: GraphQL response.
    """
    data = request.get_json()
    query = data.get("query", "")
    variables = data.get("variables", {})

    # Simple GraphQL-like response simulation
    if "users" in query.lower():
        response_data = {
            "users": [
                {"id": 1, "name": "Alice", "email": "alice@example.com"},
                {"id": 2, "name": "Bob", "email": "bob@example.com"},
                {"id": 3, "name": "Charlie", "email": "charlie@example.com"},
            ]
        }
    elif "posts" in query.lower():
        response_data = {
            "posts": [
                {"id": 1, "title": "Hello World", "content": "First post"},
                {"id": 2, "title": "GraphQL Test", "content": "Testing GraphQL"},
            ]
        }
    else:
        response_data = {"message": "Query not recognized"}

    return jsonify(
        {
            "data": response_data,
            "extensions": {
                "query": query,
                "variables": variables,
                "timestamp": datetime.utcnow().isoformat() + "Z",
            },
        }
    )


@advanced_bp.route("/advanced/multipart", methods=["POST"])
def multipart_handler():
    """Handles multipart/form-data requests.
    ---
    tags:
      - Advanced
    consumes:
      - multipart/form-data
    produces:
      - application/json
    responses:
      200:
        description: Multipart data processed.
    """
    form_data = dict(request.form)
    files_data = {}

    for key, file in request.files.items():
        files_data[key] = {
            "filename": file.filename,
            "content_type": file.content_type,
            "size": len(file.read()),
            "md5": None,  # Would calculate MD5 in real scenario
        }
        file.seek(0)  # Reset file pointer

    return jsonify(
        {
            "form_fields": form_data,
            "files": files_data,
            "total_files": len(files_data),
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }
    )


@advanced_bp.route("/advanced/csv-export", methods=["GET"])
def csv_export():
    """Returns data in CSV format.
    ---
    tags:
      - Advanced
    parameters:
      - in: query
        name: rows
        type: integer
        default: 100
    produces:
      - text/csv
    responses:
      200:
        description: CSV data.
    """
    rows = min(int(request.args.get("rows", 100)), 1000)

    output = io.StringIO()
    writer = csv.writer(output)

    # Write header
    writer.writerow(["id", "name", "email", "value", "created_at"])

    # Write data rows
    for i in range(rows):
        writer.writerow(
            [
                i + 1,
                f"User {i + 1}",
                f"user{i + 1}@example.com",
                random.randint(1, 1000),
                datetime.utcnow().isoformat() + "Z",
            ]
        )

    csv_content = output.getvalue()
    output.close()

    return Response(
        csv_content,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=export.csv"},
    )


@advanced_bp.route("/advanced/complex-validation", methods=["POST"])
def complex_validation():
    """Performs complex validation on input data.
    ---
    tags:
      - Advanced
    consumes:
      - application/json
    produces:
      - application/json
    responses:
      200:
        description: Validation results.
      422:
        description: Validation failed.
    """
    data = request.get_json()
    errors = []
    warnings = []

    # Validate required fields
    required_fields = ["name", "email", "age"]
    for field in required_fields:
        if field not in data:
            errors.append(f"Missing required field: {field}")

    # Validate email format
    if "email" in data:
        email = data["email"]
        if "@" not in email or "." not in email:
            errors.append("Invalid email format")

    # Validate age
    if "age" in data:
        try:
            age = int(data["age"])
            if age < 0:
                errors.append("Age cannot be negative")
            elif age > 150:
                warnings.append("Age seems unusually high")
        except (ValueError, TypeError):
            errors.append("Age must be a number")

    # Validate name length
    if "name" in data:
        name = data["name"]
        if len(name) < 2:
            errors.append("Name must be at least 2 characters")
        elif len(name) > 100:
            errors.append("Name cannot exceed 100 characters")

    if errors:
        return jsonify(
            {
                "valid": False,
                "errors": errors,
                "warnings": warnings,
                "timestamp": datetime.utcnow().isoformat() + "Z",
            }
        ), 422

    return jsonify(
        {
            "valid": True,
            "warnings": warnings,
            "processed_data": data,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }
    )


@advanced_bp.route(
    "/advanced/nested-resources/<int:parent_id>/items", methods=["GET", "POST"]
)
def nested_resources(parent_id):
    """Handles nested resource operations.
    ---
    tags:
      - Advanced
    parameters:
      - in: path
        name: parent_id
        type: integer
    produces:
      - application/json
    responses:
      200:
        description: Nested resource data.
    """
    if request.method == "GET":
        # Return items for the parent
        items = []
        for i in range(random.randint(1, 10)):
            items.append(
                {
                    "id": i + 1,
                    "parent_id": parent_id,
                    "name": f"Item {i + 1}",
                    "description": f"Description for item {i + 1} under parent {parent_id}",
                    "created_at": datetime.utcnow().isoformat() + "Z",
                }
            )

        return jsonify(
            {
                "parent_id": parent_id,
                "items": items,
                "total_items": len(items),
                "timestamp": datetime.utcnow().isoformat() + "Z",
            }
        )

    elif request.method == "POST":
        # Create new item under parent
        data = request.get_json()
        new_item = {
            "id": random.randint(1000, 9999),
            "parent_id": parent_id,
            "name": data.get("name", "New Item"),
            "description": data.get("description", ""),
            "created_at": datetime.utcnow().isoformat() + "Z",
        }

        return jsonify(new_item), 201


@advanced_bp.route("/advanced/bulk-operations", methods=["POST"])
def bulk_operations():
    """Handles bulk operations on multiple resources.
    ---
    tags:
      - Advanced
    consumes:
      - application/json
    produces:
      - application/json
    responses:
      200:
        description: Bulk operation results.
    """
    data = request.get_json()
    operations = data.get("operations", [])

    results = []

    for i, operation in enumerate(operations):
        op_type = operation.get("type", "unknown")
        op_data = operation.get("data", {})

        # Simulate processing each operation
        processing_time = random.uniform(0.1, 0.5)
        time.sleep(processing_time)

        success = random.random() > 0.1  # 90% success rate

        result = {
            "operation_index": i,
            "type": op_type,
            "success": success,
            "processing_time": processing_time,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }

        if success:
            result["result"] = {"id": random.randint(1000, 9999), "data": op_data}
        else:
            result["error"] = "Simulated operation failure"

        results.append(result)

    total_operations = len(operations)
    successful_operations = sum(1 for r in results if r["success"])
    failed_operations = total_operations - successful_operations

    return jsonify(
        {
            "summary": {
                "total_operations": total_operations,
                "successful": successful_operations,
                "failed": failed_operations,
                "success_rate": successful_operations / total_operations
                if total_operations > 0
                else 0,
            },
            "results": results,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }
    )


@advanced_bp.route("/advanced/sse", methods=["GET"])
def server_sent_events():
    """Server-Sent Events endpoint.
    ---
    tags:
      - Advanced
    parameters:
      - in: query
        name: events
        type: integer
        default: 10
      - in: query
        name: interval
        type: number
        default: 1.0
    produces:
      - text/event-stream
    responses:
      200:
        description: Server-sent events stream.
    """
    events = min(int(request.args.get("events", 10)), 50)
    interval = min(float(request.args.get("interval", 1.0)), 5.0)

    def event_stream():
        for i in range(events):
            event_data = {
                "event_id": i + 1,
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "data": f"Event {i + 1} of {events}",
                "random_value": random.randint(1, 100),
            }

            yield f"data: {json.dumps(event_data)}\n\n"

            if i < events - 1:  # Don't delay after last event
                time.sleep(interval)

        # Send final event
        yield 'event: complete\ndata: {"message": "Stream complete"}\n\n'

    return Response(
        event_stream(),
        mimetype="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"},
    )


@advanced_bp.route("/advanced/conditional", methods=["GET", "POST"])
def conditional_response():
    """Returns different responses based on conditions.
    ---
    tags:
      - Advanced
    parameters:
      - in: header
        name: X-Test-Mode
        type: string
      - in: query
        name: format
        type: string
        enum: [json, xml, text]
        default: json
    produces:
      - application/json
      - application/xml
      - text/plain
    responses:
      200:
        description: Conditional response.
    """
    test_mode = request.headers.get("X-Test-Mode", "normal")
    response_format = request.args.get("format", "json")

    data = {
        "mode": test_mode,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "user_agent": request.headers.get("User-Agent", "Unknown"),
        "ip": request.remote_addr,
    }

    if test_mode == "debug":
        data["debug_info"] = {
            "all_headers": dict(request.headers),
            "all_args": dict(request.args),
            "method": request.method,
        }

    if response_format == "xml":
        xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<response>
    <mode>{data["mode"]}</mode>
    <timestamp>{data["timestamp"]}</timestamp>
    <user_agent>{data["user_agent"]}</user_agent>
    <ip>{data["ip"]}</ip>
</response>"""
        return Response(xml_content, mimetype="application/xml")

    elif response_format == "text":
        text_content = f"Mode: {data['mode']}\nTimestamp: {data['timestamp']}\nUser-Agent: {data['user_agent']}\nIP: {data['ip']}"
        return Response(text_content, mimetype="text/plain")

    else:  # json
        return jsonify(data)
