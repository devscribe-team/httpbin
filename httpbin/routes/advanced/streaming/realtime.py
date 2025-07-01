# -*- coding: utf-8 -*-

"""
httpbin.routes.advanced.streaming.realtime
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Real-time streaming and WebSocket-like functionality.
"""

import json
import random
import time
from datetime import datetime

from flask import Blueprint, Response, jsonify, request

realtime_bp = Blueprint("realtime", __name__)


@realtime_bp.route("/realtime/feed", methods=["GET"])
def live_data_feed():
    """Simulates a live data feed.
    ---
    tags:
      - Real-time
    parameters:
      - in: query
        name: feed_type
        type: string
        enum: [stock, weather, social, metrics]
        default: metrics
      - in: query
        name: duration
        type: integer
        default: 30
        description: Feed duration in seconds
    produces:
      - application/json
    responses:
      200:
        description: Live data feed.
    """
    feed_type = request.args.get("feed_type", "metrics")
    duration = min(int(request.args.get("duration", 30)), 120)  # Max 2 minutes

    def generate_feed():
        start_time = time.time()
        counter = 0

        while time.time() - start_time < duration:
            counter += 1

            if feed_type == "stock":
                data = {
                    "symbol": random.choice(["AAPL", "GOOGL", "MSFT", "TSLA"]),
                    "price": round(random.uniform(100, 300), 2),
                    "change": round(random.uniform(-5, 5), 2),
                    "volume": random.randint(1000, 100000),
                }
            elif feed_type == "weather":
                data = {
                    "city": random.choice(["New York", "London", "Tokyo", "Sydney"]),
                    "temperature": round(random.uniform(-10, 35), 1),
                    "humidity": random.randint(30, 90),
                    "pressure": round(random.uniform(980, 1020), 1),
                }
            elif feed_type == "social":
                data = {
                    "platform": random.choice(["twitter", "facebook", "instagram"]),
                    "mentions": random.randint(0, 1000),
                    "sentiment": random.choice(["positive", "negative", "neutral"]),
                    "reach": random.randint(100, 50000),
                }
            else:  # metrics
                data = {
                    "cpu_usage": round(random.uniform(10, 90), 1),
                    "memory_usage": round(random.uniform(30, 80), 1),
                    "disk_io": random.randint(0, 1000),
                    "network_io": random.randint(0, 10000),
                }

            feed_item = {
                "id": counter,
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "feed_type": feed_type,
                "data": data,
            }

            yield f"data: {json.dumps(feed_item)}\n\n"
            time.sleep(1)  # Update every second

    return Response(
        generate_feed(),
        mimetype="text/plain",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"},
    )


@realtime_bp.route("/realtime/notifications", methods=["GET"])
def notification_stream():
    """Simulates push notifications.
    ---
    tags:
      - Real-time
    parameters:
      - in: query
        name: frequency
        type: number
        default: 2.0
        description: Notification frequency in seconds
      - in: query
        name: count
        type: integer
        default: 10
        description: Number of notifications
    produces:
      - text/event-stream
    responses:
      200:
        description: Notification stream.
    """
    frequency = max(0.5, float(request.args.get("frequency", 2.0)))
    count = min(int(request.args.get("count", 10)), 50)

    def generate_notifications():
        for i in range(count):
            notification_types = ["message", "alert", "reminder", "update", "warning"]

            notification = {
                "id": i + 1,
                "type": random.choice(notification_types),
                "title": f"Notification {i + 1}",
                "message": f"This is notification number {i + 1}",
                "priority": random.choice(["low", "medium", "high"]),
                "timestamp": datetime.utcnow().isoformat() + "Z",
            }

            yield "event: notification\n"
            yield f"data: {json.dumps(notification)}\n\n"

            if i < count - 1:
                time.sleep(frequency)

        # Send completion event
        yield "event: complete\n"
        yield 'data: {"message": "All notifications sent"}\n\n'

    return Response(
        generate_notifications(),
        mimetype="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"},
    )


@realtime_bp.route("/realtime/chat", methods=["POST"])
def chat_simulation():
    """Simulates a chat conversation.
    ---
    tags:
      - Real-time
    consumes:
      - application/json
    produces:
      - application/json
    responses:
      200:
        description: Chat simulation response.
    """
    data = request.get_json()
    user_message = data.get("message", "")
    user_id = data.get("user_id", "anonymous")

    # Simulate chat bot responses
    bot_responses = [
        "That's interesting! Tell me more.",
        "I understand what you mean.",
        "Could you clarify that point?",
        "Thanks for sharing that information.",
        "I see your perspective on this.",
        "That's a great question!",
        "Let me think about that...",
        "I appreciate your input.",
    ]

    # Simulate processing delay
    time.sleep(random.uniform(0.5, 2.0))

    response_message = random.choice(bot_responses)

    return jsonify(
        {
            "conversation_id": f"chat_{random.randint(1000, 9999)}",
            "user_message": user_message,
            "user_id": user_id,
            "bot_response": response_message,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "response_time": random.uniform(0.5, 2.0),
        }
    )


@realtime_bp.route("/realtime/status", methods=["GET"])
def system_status_stream():
    """Provides real-time system status updates.
    ---
    tags:
      - Real-time
    parameters:
      - in: query
        name: interval
        type: number
        default: 3.0
        description: Update interval in seconds
      - in: query
        name: duration
        type: integer
        default: 60
        description: Stream duration in seconds
    produces:
      - text/event-stream
    responses:
      200:
        description: System status stream.
    """
    interval = max(1.0, float(request.args.get("interval", 3.0)))
    duration = min(int(request.args.get("duration", 60)), 300)  # Max 5 minutes

    def generate_status():
        start_time = time.time()
        update_count = 0

        while time.time() - start_time < duration:
            update_count += 1

            status = {
                "update_id": update_count,
                "system_health": random.choice(["healthy", "warning", "critical"]),
                "services": {
                    "database": random.choice(["online", "slow", "offline"]),
                    "cache": random.choice(["online", "degraded"]),
                    "api": random.choice(["online", "rate_limited"]),
                    "storage": random.choice(["online", "low_space"]),
                },
                "metrics": {
                    "active_users": random.randint(50, 500),
                    "requests_per_minute": random.randint(100, 2000),
                    "error_rate": round(random.uniform(0, 5), 2),
                    "response_time": round(random.uniform(50, 500), 1),
                },
                "timestamp": datetime.utcnow().isoformat() + "Z",
            }

            yield "event: status_update\n"
            yield f"data: {json.dumps(status)}\n\n"

            time.sleep(interval)

        # Send completion event
        yield "event: stream_end\n"
        yield f'data: {{"message": "Status stream ended", "total_updates": {update_count}}}\n\n'

    return Response(
        generate_status(),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
        },
    )
