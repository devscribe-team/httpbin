# -*- coding: utf-8 -*-

"""
httpbin.simulation_routes
~~~~~~~~~~~~~~~~~~~~~~~~~

Routes that simulate various testing scenarios and edge cases.
"""

import random
import time
import uuid
from datetime import datetime

from flask import Blueprint, jsonify, request

sim_bp = Blueprint("simulation", __name__)


@sim_bp.route("/simulate/slow", methods=["GET", "POST"])
def slow_response():
    """Simulates a slow response for testing timeouts.
    ---
    tags:
      - Simulation
    parameters:
      - in: query
        name: delay
        type: integer
        default: 5
        description: Delay in seconds (max 30)
    produces:
      - application/json
    responses:
      200:
        description: Delayed response.
    """
    delay = min(int(request.args.get("delay", 5)), 30)
    start_time = datetime.utcnow()

    time.sleep(delay)

    end_time = datetime.utcnow()

    return jsonify(
        {
            "message": f"Response delayed by {delay} seconds",
            "requested_delay": delay,
            "actual_delay": (end_time - start_time).total_seconds(),
            "start_time": start_time.isoformat() + "Z",
            "end_time": end_time.isoformat() + "Z",
        }
    )


@sim_bp.route("/simulate/random-status", methods=["GET", "POST", "PUT", "DELETE"])
def random_status():
    """Returns random HTTP status codes for testing error handling.
    ---
    tags:
      - Simulation
    parameters:
      - in: query
        name: codes
        type: string
        default: "200,404,500"
        description: Comma-separated list of status codes to randomly choose from
    produces:
      - application/json
    responses:
      200:
        description: Random status response.
    """
    codes_param = request.args.get("codes", "200,404,500")
    try:
        codes = [int(code.strip()) for code in codes_param.split(",")]
    except ValueError:
        return jsonify({"error": "Invalid status codes"}), 400

    chosen_code = random.choice(codes)

    response_data = {
        "status": chosen_code,
        "message": f"Randomly selected status code {chosen_code}",
        "available_codes": codes,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }

    return jsonify(response_data), chosen_code


@sim_bp.route("/simulate/fail/<float:probability>", methods=["GET", "POST"])
def random_failure(probability):
    """Randomly fails based on probability for testing resilience.
    ---
    tags:
      - Simulation
    parameters:
      - in: path
        name: probability
        type: number
        description: Probability of failure (0.0 to 1.0)
    produces:
      - application/json
    responses:
      200:
        description: Success response.
      500:
        description: Simulated failure.
    """
    probability = max(0.0, min(1.0, probability))

    if random.random() < probability:
        return jsonify(
            {
                "error": "Simulated failure",
                "probability": probability,
                "message": "This endpoint randomly failed",
                "timestamp": datetime.utcnow().isoformat() + "Z",
            }
        ), 500

    return jsonify(
        {
            "success": True,
            "probability": probability,
            "message": "Request succeeded despite failure probability",
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }
    )


@sim_bp.route("/simulate/large-response", methods=["GET"])
def large_response():
    """Returns a large response for testing data handling.
    ---
    tags:
      - Simulation
    parameters:
      - in: query
        name: size
        type: integer
        default: 1000
        description: Number of items to include (max 10000)
    produces:
      - application/json
    responses:
      200:
        description: Large response data.
    """
    size = min(int(request.args.get("size", 1000)), 10000)

    items = []
    for i in range(size):
        items.append(
            {
                "id": i,
                "name": f"Item {i}",
                "description": f"This is a description for item {i} "
                * 10,  # Make it longer
                "value": random.uniform(0, 1000),
                "category": random.choice(["A", "B", "C", "D"]),
                "tags": [f"tag{j}" for j in range(random.randint(1, 5))],
                "metadata": {
                    "created": datetime.utcnow().isoformat() + "Z",
                    "updated": datetime.utcnow().isoformat() + "Z",
                    "version": random.randint(1, 10),
                },
            }
        )

    return jsonify({"total_items": len(items), "requested_size": size, "items": items})


@sim_bp.route("/simulate/memory-test", methods=["POST"])
def memory_test():
    """Tests memory usage by processing large data.
    ---
    tags:
      - Simulation
    consumes:
      - application/json
    produces:
      - application/json
    responses:
      200:
        description: Memory test results.
    """
    data = request.get_json()
    operation = data.get("operation", "duplicate")
    size = min(int(data.get("size", 1000)), 5000)

    # Generate test data
    test_data = [f"test_string_{i}" * 10 for i in range(size)]

    if operation == "duplicate":
        result = test_data * 2
    elif operation == "reverse":
        result = [s[::-1] for s in test_data]
    elif operation == "sort":
        result = sorted(test_data)
    elif operation == "concatenate":
        result = ["".join(test_data)]
    else:
        result = test_data

    return jsonify(
        {
            "operation": operation,
            "input_size": len(test_data),
            "output_size": len(result),
            "memory_test_completed": True,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }
    )


@sim_bp.route("/simulate/concurrent/<int:session_id>", methods=["GET", "POST"])
def concurrent_session(session_id):
    """Simulates concurrent sessions for testing race conditions.
    ---
    tags:
      - Simulation
    parameters:
      - in: path
        name: session_id
        type: integer
    produces:
      - application/json
    responses:
      200:
        description: Session response.
    """
    # Simulate some processing time
    processing_time = random.uniform(0.1, 2.0)
    time.sleep(processing_time)

    return jsonify(
        {
            "session_id": session_id,
            "processing_time": processing_time,
            "thread_safe": True,
            "concurrent_requests_handled": True,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "request_id": str(uuid.uuid4()),
        }
    )


@sim_bp.route("/simulate/rate-limit", methods=["GET", "POST"])
def rate_limit_test():
    """Simulates rate limiting for testing throttling.
    ---
    tags:
      - Simulation
    parameters:
      - in: query
        name: limit
        type: integer
        default: 10
        description: Requests per minute limit
    produces:
      - application/json
    responses:
      200:
        description: Request within rate limit.
      429:
        description: Rate limit exceeded.
    """
    limit = int(request.args.get("limit", 10))

    # Simulate rate limiting (randomly trigger based on time)
    current_minute = datetime.utcnow().minute
    request_count = (current_minute + random.randint(1, 15)) % limit

    if request_count >= limit:
        return jsonify(
            {
                "error": "Rate limit exceeded",
                "limit": limit,
                "retry_after": 60,
                "current_count": request_count,
            }
        ), 429

    return jsonify(
        {
            "success": True,
            "rate_limit": limit,
            "current_count": request_count,
            "remaining": limit - request_count,
            "reset_time": datetime.utcnow().replace(second=0, microsecond=0).isoformat()
            + "Z",
        }
    )


@sim_bp.route("/simulate/auth-required", methods=["GET", "POST"])
def auth_required():
    """Simulates endpoints requiring authentication.
    ---
    tags:
      - Simulation
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
    produces:
      - application/json
    responses:
      200:
        description: Authenticated response.
      401:
        description: Authentication required.
    """
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return jsonify(
            {
                "error": "Authentication required",
                "message": "Missing Authorization header",
            }
        ), 401

    if not auth_header.startswith("Bearer "):
        return jsonify(
            {
                "error": "Invalid authentication",
                "message": "Authorization must be Bearer token",
            }
        ), 401

    token = auth_header[7:]  # Remove 'Bearer '

    # Simple token validation (anything with 'valid' in it)
    if "valid" not in token.lower():
        return jsonify(
            {"error": "Invalid token", "message": "Token validation failed"}
        ), 401

    return jsonify(
        {
            "authenticated": True,
            "user": "test_user",
            "token_preview": token[:10] + "...",
            "permissions": ["read", "write"],
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }
    )


@sim_bp.route("/simulate/circuit-breaker", methods=["GET"])
def circuit_breaker():
    """Simulates circuit breaker pattern for testing resilience.
    ---
    tags:
      - Simulation
    parameters:
      - in: query
        name: state
        type: string
        enum: [closed, open, half-open]
        default: closed
    produces:
      - application/json
    responses:
      200:
        description: Service available.
      503:
        description: Service unavailable (circuit open).
    """
    state = request.args.get("state", "closed").lower()

    if state == "open":
        return jsonify(
            {
                "error": "Service unavailable",
                "circuit_breaker_state": "open",
                "message": "Circuit breaker is open, service temporarily unavailable",
                "retry_after": 30,
            }
        ), 503

    elif state == "half-open":
        # 50% chance of success in half-open state
        if random.random() < 0.5:
            return jsonify(
                {
                    "success": True,
                    "circuit_breaker_state": "half-open",
                    "message": "Request succeeded, circuit may close",
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                }
            )
        else:
            return jsonify(
                {
                    "error": "Service failed",
                    "circuit_breaker_state": "half-open -> open",
                    "message": "Request failed, circuit reopened",
                    "retry_after": 30,
                }
            ), 503

    else:  # closed state
        return jsonify(
            {
                "success": True,
                "circuit_breaker_state": "closed",
                "message": "Service operating normally",
                "timestamp": datetime.utcnow().isoformat() + "Z",
            }
        )
