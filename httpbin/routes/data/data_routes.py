# -*- coding: utf-8 -*-

"""
httpbin.data_routes
~~~~~~~~~~~~~~~~~~~

Data manipulation and testing routes.
"""

import base64
import hashlib
import random
import string

from flask import Blueprint, Response, jsonify, request

data_bp = Blueprint("data", __name__)


@data_bp.route("/data/generate/<data_type>", methods=["GET"])
def generate_data(data_type):
    """Generate various types of test data.
    ---
    tags:
      - Data Generation
    parameters:
      - in: path
        name: data_type
        type: string
        enum: [names, emails, numbers, words, sentences]
      - in: query
        name: count
        type: integer
        default: 10
    produces:
      - application/json
    responses:
      200:
        description: Generated test data.
    """
    count = int(request.args.get("count", 10))
    count = min(count, 1000)  # Limit to 1000 items

    data = []

    if data_type == "names":
        first_names = [
            "John",
            "Jane",
            "Bob",
            "Alice",
            "Charlie",
            "Diana",
            "Eve",
            "Frank",
        ]
        last_names = [
            "Smith",
            "Johnson",
            "Williams",
            "Brown",
            "Jones",
            "Garcia",
            "Miller",
        ]
        for _ in range(count):
            data.append(f"{random.choice(first_names)} {random.choice(last_names)}")

    elif data_type == "emails":
        domains = ["example.com", "test.org", "demo.net", "fake.io"]
        for i in range(count):
            username = "".join(random.choices(string.ascii_lowercase, k=8))
            data.append(f"{username}@{random.choice(domains)}")

    elif data_type == "numbers":
        for _ in range(count):
            data.append(random.randint(1, 10000))

    elif data_type == "words":
        words = [
            "apple",
            "banana",
            "cherry",
            "date",
            "elderberry",
            "fig",
            "grape",
            "honeydew",
        ]
        for _ in range(count):
            data.append(random.choice(words))

    elif data_type == "sentences":
        subjects = ["The cat", "A dog", "The bird", "An elephant"]
        verbs = ["runs", "jumps", "flies", "sleeps", "eats"]
        objects = ["quickly", "happily", "silently", "loudly"]
        for _ in range(count):
            data.append(
                f"{random.choice(subjects)} {random.choice(verbs)} {random.choice(objects)}."
            )

    else:
        return jsonify({"error": "Invalid data type"}), 400

    return jsonify({"type": data_type, "count": len(data), "data": data})


@data_bp.route("/data/transform", methods=["POST"])
def transform_data():
    """Transform input data in various ways.
    ---
    tags:
      - Data Transformation
    consumes:
      - application/json
    produces:
      - application/json
    responses:
      200:
        description: Transformed data.
    """
    data = request.get_json()
    transform_type = data.get("transform", "uppercase")
    input_data = data.get("data", [])

    result = []

    if transform_type == "uppercase":
        result = [str(item).upper() for item in input_data]
    elif transform_type == "lowercase":
        result = [str(item).lower() for item in input_data]
    elif transform_type == "reverse":
        result = [str(item)[::-1] for item in input_data]
    elif transform_type == "hash":
        result = [hashlib.md5(str(item).encode()).hexdigest() for item in input_data]
    elif transform_type == "base64":
        result = [base64.b64encode(str(item).encode()).decode() for item in input_data]
    elif transform_type == "length":
        result = [len(str(item)) for item in input_data]
    else:
        return jsonify({"error": "Invalid transform type"}), 400

    return jsonify(
        {
            "transform": transform_type,
            "original_count": len(input_data),
            "transformed_count": len(result),
            "result": result,
        }
    )


@data_bp.route("/data/validate", methods=["POST"])
def validate_data():
    """Validate data against various rules.
    ---
    tags:
      - Data Validation
    consumes:
      - application/json
    produces:
      - application/json
    responses:
      200:
        description: Validation results.
    """
    data = request.get_json()
    validation_type = data.get("type", "email")
    items = data.get("items", [])

    results = []

    for item in items:
        valid = False
        reason = ""

        if validation_type == "email":
            valid = "@" in str(item) and "." in str(item)
            reason = "Valid email format" if valid else "Invalid email format"
        elif validation_type == "phone":
            # Simple phone validation
            digits = "".join(filter(str.isdigit, str(item)))
            valid = len(digits) >= 10
            reason = "Valid phone number" if valid else "Phone number too short"
        elif validation_type == "url":
            valid = str(item).startswith(("http://", "https://"))
            reason = "Valid URL" if valid else "URL must start with http:// or https://"
        elif validation_type == "positive_number":
            try:
                valid = float(item) > 0
                reason = "Valid positive number" if valid else "Number must be positive"
            except (ValueError, TypeError):
                valid = False
                reason = "Not a valid number"

        results.append({"item": item, "valid": valid, "reason": reason})

    valid_count = sum(1 for r in results if r["valid"])

    return jsonify(
        {
            "validation_type": validation_type,
            "total_items": len(results),
            "valid_items": valid_count,
            "invalid_items": len(results) - valid_count,
            "results": results,
        }
    )


@data_bp.route("/data/aggregate", methods=["POST"])
def aggregate_data():
    """Perform aggregation operations on data.
    ---
    tags:
      - Data Aggregation
    consumes:
      - application/json
    produces:
      - application/json
    responses:
      200:
        description: Aggregation results.
    """
    data = request.get_json()
    numbers = data.get("numbers", [])
    operation = data.get("operation", "sum")

    try:
        numeric_values = [
            float(x)
            for x in numbers
            if isinstance(x, (int, float, str))
            and str(x).replace(".", "").replace("-", "").isdigit()
        ]
    except ValueError:
        return jsonify({"error": "Invalid numeric data"}), 400

    if not numeric_values:
        return jsonify({"error": "No valid numbers provided"}), 400

    result = 0

    if operation == "sum":
        result = sum(numeric_values)
    elif operation == "average" or operation == "mean":
        result = sum(numeric_values) / len(numeric_values)
    elif operation == "min":
        result = min(numeric_values)
    elif operation == "max":
        result = max(numeric_values)
    elif operation == "count":
        result = len(numeric_values)
    elif operation == "median":
        sorted_values = sorted(numeric_values)
        n = len(sorted_values)
        result = (
            sorted_values[n // 2]
            if n % 2 == 1
            else (sorted_values[n // 2 - 1] + sorted_values[n // 2]) / 2
        )
    else:
        return jsonify({"error": "Invalid operation"}), 400

    return jsonify(
        {
            "operation": operation,
            "input_count": len(numbers),
            "valid_numbers": len(numeric_values),
            "result": result,
            "statistics": {
                "min": min(numeric_values),
                "max": max(numeric_values),
                "count": len(numeric_values),
                "sum": sum(numeric_values),
            },
        }
    )


@data_bp.route("/data/format/<format_type>", methods=["POST"])
def format_data(format_type):
    """Format data in different output formats.
    ---
    tags:
      - Data Formatting
    parameters:
      - in: path
        name: format_type
        type: string
        enum: [csv, xml, yaml, table]
    consumes:
      - application/json
    produces:
      - text/plain
      - application/xml
      - text/csv
    responses:
      200:
        description: Formatted data.
    """
    data = request.get_json()
    items = data.get("items", [])

    if format_type == "csv":
        if not items:
            return "No data provided", 400

        # Assume items are dictionaries
        if isinstance(items[0], dict):
            headers = list(items[0].keys())
            csv_content = ",".join(headers) + "\n"
            for item in items:
                row = ",".join(str(item.get(h, "")) for h in headers)
                csv_content += row + "\n"
        else:
            csv_content = "\n".join(str(item) for item in items)

        return Response(csv_content, mimetype="text/csv")

    elif format_type == "xml":
        xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n<data>\n'
        for i, item in enumerate(items):
            xml_content += f'  <item id="{i}">{item}</item>\n'
        xml_content += "</data>"

        return Response(xml_content, mimetype="application/xml")

    elif format_type == "yaml":
        yaml_content = "data:\n"
        for item in items:
            yaml_content += f"  - {item}\n"

        return Response(yaml_content, mimetype="text/plain")

    elif format_type == "table":
        if not items:
            return "No data provided", 400

        # Simple ASCII table
        if isinstance(items[0], dict):
            headers = list(items[0].keys())
            table = " | ".join(headers) + "\n"
            table += "-" * len(table) + "\n"
            for item in items:
                row = " | ".join(str(item.get(h, "")) for h in headers)
                table += row + "\n"
        else:
            table = "Value\n-----\n"
            for item in items:
                table += str(item) + "\n"

        return Response(table, mimetype="text/plain")

    else:
        return jsonify({"error": "Invalid format type"}), 400


@data_bp.route("/data/filter", methods=["POST"])
def filter_data():
    """Filter data based on criteria.
    ---
    tags:
      - Data Filtering
    consumes:
      - application/json
    produces:
      - application/json
    responses:
      200:
        description: Filtered data.
    """
    data = request.get_json()
    items = data.get("items", [])
    filter_type = data.get("filter_type", "contains")
    filter_value = data.get("filter_value", "")

    filtered_items = []

    for item in items:
        item_str = str(item).lower()
        filter_str = str(filter_value).lower()

        if filter_type == "contains" and filter_str in item_str:
            filtered_items.append(item)
        elif filter_type == "starts_with" and item_str.startswith(filter_str):
            filtered_items.append(item)
        elif filter_type == "ends_with" and item_str.endswith(filter_str):
            filtered_items.append(item)
        elif filter_type == "equals" and item_str == filter_str:
            filtered_items.append(item)
        elif filter_type == "greater_than":
            try:
                if float(item) > float(filter_value):
                    filtered_items.append(item)
            except (ValueError, TypeError):
                pass
        elif filter_type == "less_than":
            try:
                if float(item) < float(filter_value):
                    filtered_items.append(item)
            except (ValueError, TypeError):
                pass

    return jsonify(
        {
            "filter_type": filter_type,
            "filter_value": filter_value,
            "original_count": len(items),
            "filtered_count": len(filtered_items),
            "filtered_items": filtered_items,
        }
    )
