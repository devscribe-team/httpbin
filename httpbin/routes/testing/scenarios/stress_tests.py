# -*- coding: utf-8 -*-

"""
httpbin.routes.testing.scenarios.stress_tests
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Specialized routes for stress testing scenarios.
"""

import gc
import json
import random
import threading
import time
from datetime import datetime

from flask import Blueprint, jsonify, request

stress_bp = Blueprint("stress", __name__)


@stress_bp.route("/stress/cpu/<int:duration>", methods=["GET"])
def cpu_intensive(duration):
    """CPU intensive operation for load testing.
    ---
    tags:
      - Stress Testing
    parameters:
      - in: path
        name: duration
        type: integer
        description: Duration in seconds (max 10)
    produces:
      - application/json
    responses:
      200:
        description: CPU intensive operation completed.
    """
    duration = min(duration, 10)  # Limit to 10 seconds
    start_time = time.time()
    end_time = start_time + duration

    operations = 0
    while time.time() < end_time:
        # Simulate CPU work
        for i in range(1000):
            _ = i**2
        operations += 1000

    actual_duration = time.time() - start_time

    return jsonify(
        {
            "requested_duration": duration,
            "actual_duration": actual_duration,
            "operations_performed": operations,
            "ops_per_second": operations / actual_duration,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }
    )


@stress_bp.route("/stress/memory/<int:mb>", methods=["GET"])
def memory_allocation(mb):
    """Allocates memory for testing memory limits.
    ---
    tags:
      - Stress Testing
    parameters:
      - in: path
        name: mb
        type: integer
        description: Memory to allocate in MB (max 100)
    produces:
      - application/json
    responses:
      200:
        description: Memory allocation test completed.
    """
    mb = min(mb, 100)  # Limit to 100MB

    try:
        # Allocate memory
        data = []
        for i in range(mb):
            # Allocate roughly 1MB chunks
            chunk = "x" * (1024 * 1024)
            data.append(chunk)

        memory_allocated = len(data)

        # Force garbage collection to clean up
        del data
        gc.collect()

        return jsonify(
            {
                "requested_mb": mb,
                "allocated_mb": memory_allocated,
                "status": "completed",
                "timestamp": datetime.utcnow().isoformat() + "Z",
            }
        )

    except MemoryError:
        return jsonify(
            {
                "error": "Memory allocation failed",
                "requested_mb": mb,
                "timestamp": datetime.utcnow().isoformat() + "Z",
            }
        ), 507


@stress_bp.route("/stress/connections/<int:count>", methods=["GET"])
def connection_simulation(count):
    """Simulates multiple concurrent connections.
    ---
    tags:
      - Stress Testing
    parameters:
      - in: path
        name: count
        type: integer
        description: Number of simulated connections (max 50)
    produces:
      - application/json
    responses:
      200:
        description: Connection simulation completed.
    """
    count = min(count, 50)  # Limit to 50 connections

    results = []
    threads = []

    def simulate_connection(conn_id):
        start_time = time.time()
        # Simulate some work
        time.sleep(random.uniform(0.1, 1.0))
        end_time = time.time()

        results.append(
            {
                "connection_id": conn_id,
                "duration": end_time - start_time,
                "timestamp": datetime.utcnow().isoformat() + "Z",
            }
        )

    # Start threads
    for i in range(count):
        thread = threading.Thread(target=simulate_connection, args=(i,))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    return jsonify(
        {
            "simulated_connections": count,
            "results": sorted(results, key=lambda x: x["connection_id"]),
            "average_duration": sum(r["duration"] for r in results) / len(results),
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }
    )


@stress_bp.route("/stress/throughput", methods=["POST"])
def throughput_test():
    """Tests data throughput capabilities.
    ---
    tags:
      - Stress Testing
    consumes:
      - application/json
    produces:
      - application/json
    responses:
      200:
        description: Throughput test results.
    """
    start_time = time.time()

    # Get request data
    data = request.get_json()

    # Simulate processing
    processed_items = 0
    if isinstance(data, dict) and "items" in data:
        items = data["items"]
        for item in items:
            # Simulate some processing work
            _ = json.dumps(item)
            processed_items += 1

    processing_time = time.time() - start_time
    throughput = processed_items / processing_time if processing_time > 0 else 0

    return jsonify(
        {
            "items_processed": processed_items,
            "processing_time": processing_time,
            "throughput_items_per_second": throughput,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }
    )


@stress_bp.route("/stress/cascade/<int:depth>", methods=["GET"])
def cascade_requests(depth):
    """Creates cascading requests for testing call depth.
    ---
    tags:
      - Stress Testing
    parameters:
      - in: path
        name: depth
        type: integer
        description: Cascade depth (max 10)
    produces:
      - application/json
    responses:
      200:
        description: Cascade test completed.
    """
    depth = min(depth, 10)  # Limit depth

    def cascade_function(current_depth):
        if current_depth <= 0:
            return {"level": 0, "message": "Base case reached"}

        # Simulate some work at this level
        time.sleep(0.1)

        # Recurse
        child_result = cascade_function(current_depth - 1)

        return {
            "level": current_depth,
            "message": f"Processing level {current_depth}",
            "child": child_result,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }

    start_time = time.time()
    result = cascade_function(depth)
    end_time = time.time()

    return jsonify(
        {
            "requested_depth": depth,
            "total_processing_time": end_time - start_time,
            "cascade_result": result,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }
    )
