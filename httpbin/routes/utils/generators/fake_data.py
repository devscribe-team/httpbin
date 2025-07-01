# -*- coding: utf-8 -*-

"""
httpbin.routes.utils.generators.fake_data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Specialized fake data generation utilities.
"""

import random
from datetime import datetime, timedelta

from flask import Blueprint, jsonify

fake_data_bp = Blueprint("fake_data", __name__)


@fake_data_bp.route("/generate/users/<int:count>", methods=["GET"])
def generate_users(count):
    """Generates fake user profiles.
    ---
    tags:
      - Data Generation
    parameters:
      - in: path
        name: count
        type: integer
        description: Number of users to generate (max 1000)
    produces:
      - application/json
    responses:
      200:
        description: Generated user profiles.
    """
    count = min(count, 1000)

    first_names = [
        "Alice",
        "Bob",
        "Charlie",
        "Diana",
        "Eve",
        "Frank",
        "Grace",
        "Henry",
        "Ivy",
        "Jack",
        "Kate",
        "Liam",
        "Mia",
        "Noah",
        "Olivia",
        "Peter",
        "Quinn",
        "Ruby",
        "Sam",
        "Tina",
        "Uma",
        "Victor",
        "Wendy",
        "Xander",
        "Yara",
        "Zoe",
    ]

    last_names = [
        "Anderson",
        "Brown",
        "Clark",
        "Davis",
        "Evans",
        "Foster",
        "Garcia",
        "Harris",
        "Johnson",
        "King",
        "Lee",
        "Miller",
        "Nelson",
        "O'Connor",
        "Parker",
        "Quinn",
        "Rodriguez",
        "Smith",
        "Taylor",
        "Underwood",
        "Valdez",
        "Wilson",
        "Xavier",
        "Young",
        "Zhang",
    ]

    domains = ["example.com", "test.org", "demo.net", "sample.io", "fake.co"]

    users = []
    for i in range(count):
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)

        user = {
            "id": i + 1,
            "first_name": first_name,
            "last_name": last_name,
            "full_name": f"{first_name} {last_name}",
            "email": f"{first_name.lower()}.{last_name.lower()}{random.randint(1, 999)}@{random.choice(domains)}",
            "age": random.randint(18, 80),
            "phone": f"+1-{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
            "address": {
                "street": f"{random.randint(1, 9999)} {random.choice(['Main', 'Oak', 'Pine', 'Elm', 'Cedar'])} {random.choice(['St', 'Ave', 'Blvd', 'Dr'])}",
                "city": random.choice(
                    [
                        "New York",
                        "Los Angeles",
                        "Chicago",
                        "Houston",
                        "Phoenix",
                        "Philadelphia",
                    ]
                ),
                "state": random.choice(["NY", "CA", "IL", "TX", "AZ", "PA"]),
                "zip_code": f"{random.randint(10000, 99999)}",
            },
            "occupation": random.choice(
                [
                    "Engineer",
                    "Doctor",
                    "Teacher",
                    "Designer",
                    "Manager",
                    "Developer",
                    "Analyst",
                    "Consultant",
                    "Writer",
                    "Artist",
                ]
            ),
            "salary": random.randint(30000, 150000),
            "created_at": (
                datetime.utcnow() - timedelta(days=random.randint(1, 1000))
            ).isoformat()
            + "Z",
        }
        users.append(user)

    return jsonify(
        {
            "users": users,
            "count": len(users),
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }
    )


@fake_data_bp.route("/generate/products/<int:count>", methods=["GET"])
def generate_products(count):
    """Generates fake product data.
    ---
    tags:
      - Data Generation
    parameters:
      - in: path
        name: count
        type: integer
        description: Number of products to generate (max 500)
    produces:
      - application/json
    responses:
      200:
        description: Generated product data.
    """
    count = min(count, 500)

    adjectives = [
        "Amazing",
        "Premium",
        "Professional",
        "Deluxe",
        "Essential",
        "Ultimate",
        "Smart",
        "Advanced",
    ]
    nouns = [
        "Widget",
        "Gadget",
        "Tool",
        "Device",
        "System",
        "Solution",
        "Platform",
        "Software",
    ]
    categories = [
        "Electronics",
        "Software",
        "Hardware",
        "Accessories",
        "Tools",
        "Games",
        "Books",
        "Clothing",
    ]
    brands = [
        "TechCorp",
        "InnovateLab",
        "FutureTech",
        "SmartSystems",
        "ProTools",
        "NextGen",
        "EliteDevices",
    ]

    products = []
    for i in range(count):
        name = f"{random.choice(adjectives)} {random.choice(nouns)}"

        product = {
            "id": i + 1,
            "name": name,
            "sku": f"SKU-{random.randint(100000, 999999)}",
            "brand": random.choice(brands),
            "category": random.choice(categories),
            "price": round(random.uniform(9.99, 999.99), 2),
            "cost": round(random.uniform(5.00, 500.00), 2),
            "description": f"This is a high-quality {name.lower()} designed for professional use.",
            "features": [f"Feature {j + 1}" for j in range(random.randint(3, 8))],
            "specifications": {
                "weight": f"{round(random.uniform(0.1, 10.0), 1)} lbs",
                "dimensions": f"{random.randint(5, 20)} x {random.randint(5, 20)} x {random.randint(2, 10)} inches",
                "color": random.choice(
                    ["Black", "White", "Silver", "Blue", "Red", "Green"]
                ),
                "material": random.choice(
                    ["Plastic", "Metal", "Glass", "Composite", "Ceramic"]
                ),
            },
            "stock_quantity": random.randint(0, 1000),
            "rating": round(random.uniform(1.0, 5.0), 1),
            "reviews_count": random.randint(0, 500),
            "tags": random.sample(
                ["new", "popular", "sale", "featured", "recommended", "bestseller"],
                random.randint(1, 3),
            ),
            "created_at": (
                datetime.utcnow() - timedelta(days=random.randint(1, 365))
            ).isoformat()
            + "Z",
        }
        products.append(product)

    return jsonify(
        {
            "products": products,
            "count": len(products),
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }
    )


@fake_data_bp.route("/generate/transactions/<int:count>", methods=["GET"])
def generate_transactions(count):
    """Generates fake transaction data.
    ---
    tags:
      - Data Generation
    parameters:
      - in: path
        name: count
        type: integer
        description: Number of transactions to generate (max 1000)
    produces:
      - application/json
    responses:
      200:
        description: Generated transaction data.
    """
    count = min(count, 1000)

    transaction_types = [
        "purchase",
        "refund",
        "payment",
        "transfer",
        "deposit",
        "withdrawal",
    ]
    currencies = ["USD", "EUR", "GBP", "JPY", "CAD", "AUD"]
    merchants = [
        "Amazon",
        "Walmart",
        "Target",
        "Best Buy",
        "Starbucks",
        "McDonald's",
        "Shell",
        "Uber",
    ]

    transactions = []
    for i in range(count):
        transaction_type = random.choice(transaction_types)
        amount = round(random.uniform(5.00, 500.00), 2)

        if transaction_type in ["refund", "withdrawal"]:
            amount = -amount

        transaction = {
            "id": f"txn_{random.randint(100000, 999999)}",
            "type": transaction_type,
            "amount": amount,
            "currency": random.choice(currencies),
            "merchant": random.choice(merchants),
            "description": f"{transaction_type.title()} at {random.choice(merchants)}",
            "status": random.choice(["completed", "pending", "failed", "cancelled"]),
            "payment_method": random.choice(
                ["credit_card", "debit_card", "paypal", "bank_transfer", "cash"]
            ),
            "customer_id": f"cust_{random.randint(10000, 99999)}",
            "location": {
                "city": random.choice(
                    ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"]
                ),
                "country": "USA",
                "coordinates": {
                    "lat": round(random.uniform(25.0, 50.0), 6),
                    "lng": round(random.uniform(-125.0, -70.0), 6),
                },
            },
            "metadata": {
                "ip_address": f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}",
                "user_agent": "Mozilla/5.0 (compatible; API-Client/1.0)",
                "session_id": f"sess_{random.randint(100000, 999999)}",
            },
            "created_at": (
                datetime.utcnow() - timedelta(hours=random.randint(1, 720))
            ).isoformat()
            + "Z",
        }
        transactions.append(transaction)

    return jsonify(
        {
            "transactions": transactions,
            "count": len(transactions),
            "total_amount": sum(t["amount"] for t in transactions),
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }
    )


@fake_data_bp.route("/generate/events/<int:count>", methods=["GET"])
def generate_events(count):
    """Generates fake event/log data.
    ---
    tags:
      - Data Generation
    parameters:
      - in: path
        name: count
        type: integer
        description: Number of events to generate (max 1000)
    produces:
      - application/json
    responses:
      200:
        description: Generated event data.
    """
    count = min(count, 1000)

    event_types = [
        "user_login",
        "user_logout",
        "api_call",
        "error",
        "warning",
        "info",
        "debug",
    ]
    severity_levels = ["low", "medium", "high", "critical"]
    sources = [
        "web_app",
        "mobile_app",
        "api_server",
        "database",
        "cache",
        "auth_service",
    ]

    events = []
    for i in range(count):
        event_type = random.choice(event_types)

        event = {
            "id": f"evt_{random.randint(100000, 999999)}",
            "timestamp": (
                datetime.utcnow() - timedelta(minutes=random.randint(1, 1440))
            ).isoformat()
            + "Z",
            "type": event_type,
            "severity": random.choice(severity_levels),
            "source": random.choice(sources),
            "message": f"{event_type.replace('_', ' ').title()} event occurred",
            "details": {
                "user_id": f"user_{random.randint(1000, 9999)}"
                if "user" in event_type
                else None,
                "endpoint": f"/api/v1/{random.choice(['users', 'products', 'orders'])}"
                if event_type == "api_call"
                else None,
                "error_code": random.randint(400, 599)
                if event_type == "error"
                else None,
                "response_time": round(random.uniform(10, 5000), 2)
                if event_type == "api_call"
                else None,
            },
            "tags": random.sample(
                ["production", "staging", "development", "monitoring", "security"],
                random.randint(1, 2),
            ),
            "count": random.randint(1, 10),
        }

        # Remove None values from details
        event["details"] = {k: v for k, v in event["details"].items() if v is not None}

        events.append(event)

    return jsonify(
        {
            "events": events,
            "count": len(events),
            "event_types": list(set(e["type"] for e in events)),
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }
    )
