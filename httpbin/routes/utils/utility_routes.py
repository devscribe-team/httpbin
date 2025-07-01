# -*- coding: utf-8 -*-

"""
httpbin.utility_routes
~~~~~~~~~~~~~~~~~~~~~~

Utility and miscellaneous API routes for testing.
"""

import base64
import hashlib
import json
import random
import re
import string
from datetime import datetime

from flask import Blueprint, jsonify, request

util_bp = Blueprint("utility", __name__)


@util_bp.route("/util/health", methods=["GET"])
def health_check():
    """Basic health check endpoint.
    ---
    tags:
      - Utility
    produces:
      - application/json
    responses:
      200:
        description: Service health status.
    """
    return jsonify(
        {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "version": "1.0.0",
            "uptime": random.randint(100, 10000),
            "checks": {"database": "ok", "cache": "ok", "external_api": "ok"},
        }
    )


@util_bp.route("/util/version", methods=["GET"])
def version_info():
    """Returns version and build information.
    ---
    tags:
      - Utility
    produces:
      - application/json
    responses:
      200:
        description: Version information.
    """
    return jsonify(
        {
            "version": "2.1.0",
            "build": "abc123def",
            "build_date": "2024-01-15T10:30:00Z",
            "environment": "test",
            "features": ["auth", "caching", "rate_limiting"],
            "dependencies": {"flask": "2.3.0", "requests": "2.31.0", "redis": "4.5.0"},
        }
    )


@util_bp.route("/util/ping", methods=["GET", "POST"])
def ping():
    """Simple ping endpoint for connectivity tests.
    ---
    tags:
      - Utility
    produces:
      - application/json
    responses:
      200:
        description: Pong response.
    """
    return jsonify(
        {
            "message": "pong",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "method": request.method,
            "client_ip": request.remote_addr,
        }
    )


@util_bp.route("/util/echo", methods=["GET", "POST", "PUT", "PATCH"])
def echo():
    """Echoes back request data for debugging.
    ---
    tags:
      - Utility
    produces:
      - application/json
    responses:
      200:
        description: Echoed request data.
    """
    response_data = {
        "method": request.method,
        "url": request.url,
        "headers": dict(request.headers),
        "args": dict(request.args),
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }

    if request.method in ["POST", "PUT", "PATCH"]:
        if request.is_json:
            response_data["json"] = request.get_json()
        else:
            response_data["form"] = dict(request.form)
            response_data["data"] = (
                request.data.decode("utf-8") if request.data else None
            )

    return jsonify(response_data)


@util_bp.route("/util/hash", methods=["POST"])
def hash_data():
    """Generates hashes for input data.
    ---
    tags:
      - Utility
    consumes:
      - application/json
    produces:
      - application/json
    responses:
      200:
        description: Hash results.
    """
    data = request.get_json()
    text = data.get("text", "")
    algorithms = data.get("algorithms", ["md5", "sha1", "sha256"])

    results = {}

    for algo in algorithms:
        if algo == "md5":
            results["md5"] = hashlib.md5(text.encode()).hexdigest()
        elif algo == "sha1":
            results["sha1"] = hashlib.sha1(text.encode()).hexdigest()
        elif algo == "sha256":
            results["sha256"] = hashlib.sha256(text.encode()).hexdigest()
        elif algo == "sha512":
            results["sha512"] = hashlib.sha512(text.encode()).hexdigest()

    return jsonify(
        {
            "input": text,
            "hashes": results,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }
    )


@util_bp.route("/util/encode", methods=["POST"])
def encode_data():
    """Encodes data in various formats.
    ---
    tags:
      - Utility
    consumes:
      - application/json
    produces:
      - application/json
    responses:
      200:
        description: Encoded data.
    """
    data = request.get_json()
    text = data.get("text", "")
    encoding = data.get("encoding", "base64")

    result = ""

    if encoding == "base64":
        result = base64.b64encode(text.encode()).decode()
    elif encoding == "url":
        from urllib.parse import quote

        result = quote(text)
    elif encoding == "hex":
        result = text.encode().hex()
    elif encoding == "ascii":
        result = [ord(c) for c in text]
    else:
        return jsonify({"error": "Unsupported encoding"}), 400

    return jsonify(
        {
            "input": text,
            "encoding": encoding,
            "result": result,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }
    )


@util_bp.route("/util/decode", methods=["POST"])
def decode_data():
    """Decodes data from various formats.
    ---
    tags:
      - Utility
    consumes:
      - application/json
    produces:
      - application/json
    responses:
      200:
        description: Decoded data.
    """
    data = request.get_json()
    text = data.get("text", "")
    encoding = data.get("encoding", "base64")

    try:
        if encoding == "base64":
            result = base64.b64decode(text).decode()
        elif encoding == "url":
            from urllib.parse import unquote

            result = unquote(text)
        elif encoding == "hex":
            result = bytes.fromhex(text).decode()
        else:
            return jsonify({"error": "Unsupported encoding"}), 400

        return jsonify(
            {
                "input": text,
                "encoding": encoding,
                "result": result,
                "timestamp": datetime.utcnow().isoformat() + "Z",
            }
        )

    except Exception as e:
        return jsonify({"error": "Decoding failed", "message": str(e)}), 400


@util_bp.route("/util/validate-json", methods=["POST"])
def validate_json():
    """Validates JSON data.
    ---
    tags:
      - Utility
    consumes:
      - text/plain
    produces:
      - application/json
    responses:
      200:
        description: JSON validation results.
    """
    json_text = request.data.decode("utf-8")

    try:
        parsed = json.loads(json_text)
        return jsonify(
            {
                "valid": True,
                "parsed": parsed,
                "size": len(json_text),
                "type": type(parsed).__name__,
                "timestamp": datetime.utcnow().isoformat() + "Z",
            }
        )
    except json.JSONDecodeError as e:
        return jsonify(
            {
                "valid": False,
                "error": str(e),
                "line": e.lineno,
                "column": e.colno,
                "timestamp": datetime.utcnow().isoformat() + "Z",
            }
        )


@util_bp.route("/util/regex", methods=["POST"])
def regex_test():
    """Tests regular expressions against text.
    ---
    tags:
      - Utility
    consumes:
      - application/json
    produces:
      - application/json
    responses:
      200:
        description: Regex test results.
    """
    data = request.get_json()
    pattern = data.get("pattern", "")
    text = data.get("text", "")
    flags = data.get("flags", [])

    try:
        regex_flags = 0
        if "ignorecase" in flags:
            regex_flags |= re.IGNORECASE
        if "multiline" in flags:
            regex_flags |= re.MULTILINE
        if "dotall" in flags:
            regex_flags |= re.DOTALL

        compiled = re.compile(pattern, regex_flags)
        matches = compiled.findall(text)
        search_result = compiled.search(text)

        return jsonify(
            {
                "pattern": pattern,
                "text": text,
                "matches": matches,
                "match_count": len(matches),
                "first_match": {
                    "found": search_result is not None,
                    "start": search_result.start() if search_result else None,
                    "end": search_result.end() if search_result else None,
                    "groups": search_result.groups() if search_result else None,
                }
                if search_result
                else {"found": False},
                "timestamp": datetime.utcnow().isoformat() + "Z",
            }
        )

    except re.error as e:
        return jsonify({"error": "Invalid regex pattern", "message": str(e)}), 400


@util_bp.route("/util/random/<data_type>", methods=["GET"])
def random_data(data_type):
    """Generates random data of specified type.
    ---
    tags:
      - Utility
    parameters:
      - in: path
        name: data_type
        type: string
        enum: [uuid, string, number, boolean, password]
      - in: query
        name: length
        type: integer
        default: 10
      - in: query
        name: count
        type: integer
        default: 1
    produces:
      - application/json
    responses:
      200:
        description: Random data.
    """
    length = int(request.args.get("length", 10))
    count = min(int(request.args.get("count", 1)), 100)

    results = []

    for _ in range(count):
        if data_type == "uuid":
            import uuid

            results.append(str(uuid.uuid4()))
        elif data_type == "string":
            result = "".join(
                random.choices(string.ascii_letters + string.digits, k=length)
            )
            results.append(result)
        elif data_type == "number":
            results.append(random.randint(1, 10**length))
        elif data_type == "boolean":
            results.append(random.choice([True, False]))
        elif data_type == "password":
            chars = string.ascii_letters + string.digits + "!@#$%^&*"
            result = "".join(random.choices(chars, k=length))
            results.append(result)
        else:
            return jsonify({"error": "Invalid data type"}), 400

    return jsonify(
        {
            "type": data_type,
            "count": len(results),
            "length": length if data_type in ["string", "password"] else None,
            "data": results[0] if count == 1 else results,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }
    )


@util_bp.route("/util/timestamp", methods=["GET"])
def timestamp():
    """Returns current timestamp in various formats.
    ---
    tags:
      - Utility
    produces:
      - application/json
    responses:
      200:
        description: Timestamp information.
    """
    now = datetime.utcnow()

    return jsonify(
        {
            "iso": now.isoformat() + "Z",
            "unix": int(now.timestamp()),
            "formatted": now.strftime("%Y-%m-%d %H:%M:%S UTC"),
            "year": now.year,
            "month": now.month,
            "day": now.day,
            "hour": now.hour,
            "minute": now.minute,
            "second": now.second,
            "weekday": now.strftime("%A"),
            "timezone": "UTC",
        }
    )


@util_bp.route("/util/convert-time", methods=["POST"])
def convert_time():
    """Converts between different time formats.
    ---
    tags:
      - Utility
    consumes:
      - application/json
    produces:
      - application/json
    responses:
      200:
        description: Time conversion results.
    """
    data = request.get_json()
    input_time = data.get("time")
    input_format = data.get("from_format", "iso")
    output_format = data.get("to_format", "unix")

    try:
        if input_format == "unix":
            dt = datetime.fromtimestamp(int(input_time))
        elif input_format == "iso":
            dt = datetime.fromisoformat(input_time.replace("Z", ""))
        else:
            return jsonify({"error": "Unsupported input format"}), 400

        if output_format == "unix":
            result = int(dt.timestamp())
        elif output_format == "iso":
            result = dt.isoformat() + "Z"
        elif output_format == "formatted":
            result = dt.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return jsonify({"error": "Unsupported output format"}), 400

        return jsonify(
            {
                "input": input_time,
                "from_format": input_format,
                "to_format": output_format,
                "result": result,
                "timestamp": datetime.utcnow().isoformat() + "Z",
            }
        )

    except Exception as e:
        return jsonify({"error": "Time conversion failed", "message": str(e)}), 400
