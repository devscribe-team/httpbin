# -*- coding: utf-8 -*-

"""
httpbin.routes.data.formats.converters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Specialized data format conversion utilities.
"""

import csv
import io
import xml.etree.ElementTree as ET
from datetime import datetime

from flask import Blueprint, Response, jsonify, request

converters_bp = Blueprint("converters", __name__)


@converters_bp.route("/convert/json-to-csv", methods=["POST"])
def json_to_csv():
    """Converts JSON data to CSV format.
    ---
    tags:
      - Data Conversion
    consumes:
      - application/json
    produces:
      - text/csv
    responses:
      200:
        description: CSV conversion result.
    """
    data = request.get_json()

    if not isinstance(data, list) or not data:
        return jsonify({"error": "Input must be a non-empty array of objects"}), 400

    if not isinstance(data[0], dict):
        return jsonify({"error": "Array items must be objects"}), 400

    # Get all unique keys from all objects
    all_keys = set()
    for item in data:
        all_keys.update(item.keys())

    headers = sorted(list(all_keys))

    # Create CSV
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=headers)
    writer.writeheader()

    for item in data:
        # Fill missing keys with empty strings
        row = {key: item.get(key, "") for key in headers}
        writer.writerow(row)

    csv_content = output.getvalue()
    output.close()

    return Response(
        csv_content,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=converted.csv"},
    )


@converters_bp.route("/convert/csv-to-json", methods=["POST"])
def csv_to_json():
    """Converts CSV data to JSON format.
    ---
    tags:
      - Data Conversion
    consumes:
      - text/csv
    produces:
      - application/json
    responses:
      200:
        description: JSON conversion result.
    """
    csv_content = request.data.decode("utf-8")

    try:
        csv_reader = csv.DictReader(io.StringIO(csv_content))
        json_data = list(csv_reader)

        return jsonify(
            {
                "converted_data": json_data,
                "row_count": len(json_data),
                "columns": list(json_data[0].keys()) if json_data else [],
                "timestamp": datetime.utcnow().isoformat() + "Z",
            }
        )

    except Exception as e:
        return jsonify({"error": "CSV parsing failed", "message": str(e)}), 400


@converters_bp.route("/convert/json-to-xml", methods=["POST"])
def json_to_xml():
    """Converts JSON data to XML format.
    ---
    tags:
      - Data Conversion
    consumes:
      - application/json
    produces:
      - application/xml
    responses:
      200:
        description: XML conversion result.
    """
    data = request.get_json()

    def dict_to_xml(tag, d):
        elem = ET.Element(tag)
        if isinstance(d, dict):
            for key, val in d.items():
                child = dict_to_xml(key, val)
                elem.append(child)
        elif isinstance(d, list):
            for i, item in enumerate(d):
                child = dict_to_xml(f"item_{i}", item)
                elem.append(child)
        else:
            elem.text = str(d)
        return elem

    try:
        root = dict_to_xml("root", data)
        xml_string = ET.tostring(root, encoding="unicode")

        # Pretty format
        xml_content = f'<?xml version="1.0" encoding="UTF-8"?>\n{xml_string}'

        return Response(xml_content, mimetype="application/xml")

    except Exception as e:
        return jsonify({"error": "XML conversion failed", "message": str(e)}), 400


@converters_bp.route("/convert/xml-to-json", methods=["POST"])
def xml_to_json():
    """Converts XML data to JSON format.
    ---
    tags:
      - Data Conversion
    consumes:
      - application/xml
    produces:
      - application/json
    responses:
      200:
        description: JSON conversion result.
    """
    xml_content = request.data.decode("utf-8")

    def xml_to_dict(element):
        result = {}

        # Add attributes
        if element.attrib:
            result["@attributes"] = element.attrib

        # Add text content
        if element.text and element.text.strip():
            if len(element) == 0:  # No child elements
                return element.text.strip()
            else:
                result["#text"] = element.text.strip()

        # Add child elements
        for child in element:
            child_data = xml_to_dict(child)
            if child.tag in result:
                # Convert to list if multiple elements with same tag
                if not isinstance(result[child.tag], list):
                    result[child.tag] = [result[child.tag]]
                result[child.tag].append(child_data)
            else:
                result[child.tag] = child_data

        return result

    try:
        root = ET.fromstring(xml_content)
        json_data = {root.tag: xml_to_dict(root)}

        return jsonify(
            {
                "converted_data": json_data,
                "root_element": root.tag,
                "timestamp": datetime.utcnow().isoformat() + "Z",
            }
        )

    except ET.ParseError as e:
        return jsonify({"error": "XML parsing failed", "message": str(e)}), 400


@converters_bp.route("/convert/flatten", methods=["POST"])
def flatten_json():
    """Flattens nested JSON data.
    ---
    tags:
      - Data Conversion
    consumes:
      - application/json
    produces:
      - application/json
    responses:
      200:
        description: Flattened JSON data.
    """
    data = request.get_json()
    separator = request.args.get("separator", ".")

    def flatten_dict(d, parent_key="", sep="."):
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(flatten_dict(v, new_key, sep=sep).items())
            elif isinstance(v, list):
                for i, item in enumerate(v):
                    if isinstance(item, dict):
                        items.extend(
                            flatten_dict(item, f"{new_key}{sep}{i}", sep=sep).items()
                        )
                    else:
                        items.append((f"{new_key}{sep}{i}", item))
            else:
                items.append((new_key, v))
        return dict(items)

    try:
        if isinstance(data, dict):
            flattened = flatten_dict(data, sep=separator)
        else:
            return jsonify({"error": "Input must be a JSON object"}), 400

        return jsonify(
            {
                "original_keys": len(data),
                "flattened_keys": len(flattened),
                "separator": separator,
                "flattened_data": flattened,
                "timestamp": datetime.utcnow().isoformat() + "Z",
            }
        )

    except Exception as e:
        return jsonify({"error": "Flattening failed", "message": str(e)}), 400


@converters_bp.route("/convert/unflatten", methods=["POST"])
def unflatten_json():
    """Unflattens (reconstructs nested structure) flattened JSON data.
    ---
    tags:
      - Data Conversion
    consumes:
      - application/json
    produces:
      - application/json
    responses:
      200:
        description: Unflattened JSON data.
    """
    data = request.get_json()
    separator = request.args.get("separator", ".")

    def unflatten_dict(d, sep="."):
        result = {}
        for key, value in d.items():
            parts = key.split(sep)
            current = result
            for part in parts[:-1]:
                if part.isdigit():
                    part = int(part)
                    # Handle array indices
                    if not isinstance(current, list):
                        current = []
                    while len(current) <= part:
                        current.append({})
                    current = current[part]
                else:
                    if part not in current:
                        current[part] = {}
                    current = current[part]

            # Set the final value
            final_key = parts[-1]
            if final_key.isdigit():
                final_key = int(final_key)
                if not isinstance(current, list):
                    current = []
                while len(current) <= final_key:
                    current.append(None)
                current[final_key] = value
            else:
                current[final_key] = value

        return result

    try:
        if isinstance(data, dict):
            unflattened = unflatten_dict(data, sep=separator)
        else:
            return jsonify({"error": "Input must be a JSON object"}), 400

        return jsonify(
            {
                "original_keys": len(data),
                "separator": separator,
                "unflattened_data": unflattened,
                "timestamp": datetime.utcnow().isoformat() + "Z",
            }
        )

    except Exception as e:
        return jsonify({"error": "Unflattening failed", "message": str(e)}), 400
