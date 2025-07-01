# HTTPBin Routes Directory Structure

This directory contains organized API routes for testing purposes. The routes are split into logical categories for better maintainability and discoverability.

## Directory Structure

```
routes/
├── __init__.py                          # Main routes package
├── basic/                               # Basic RESTful API endpoints
│   ├── __init__.py
│   └── api_routes.py                    # Users, search, upload, batch, webhook endpoints
├── data/                                # Data manipulation and processing
│   ├── __init__.py
│   ├── data_routes.py                   # Generate, transform, validate, aggregate, filter data
│   └── formats/                         # Data format conversions
│       ├── __init__.py
│       └── converters.py                # JSON↔CSV↔XML, flatten/unflatten
├── testing/                             # Testing and simulation scenarios
│   ├── __init__.py
│   ├── simulation_routes.py             # Slow responses, failures, rate limiting, etc.
│   └── scenarios/                       # Specialized testing scenarios
│       ├── __init__.py
│       └── stress_tests.py              # CPU, memory, connection stress tests
├── utils/                               # Utility and helper endpoints
│   ├── __init__.py
│   ├── utility_routes.py                # Health, version, ping, echo, hash, encode/decode
│   └── generators/                      # Fake data generation
│       ├── __init__.py
│       └── fake_data.py                 # Generate users, products, transactions, events
└── advanced/                            # Advanced testing scenarios
    ├── __init__.py
    ├── advanced_routes.py               # Pagination, GraphQL, validation, bulk ops
    └── streaming/                       # Real-time and streaming
        ├── __init__.py
        └── realtime.py                  # Live feeds, notifications, SSE, chat
```

## Route Categories

### Basic Routes (`/api/*`)
- **Users**: CRUD operations, search functionality
- **File uploads**: Multipart form handling
- **Batch operations**: Bulk data processing
- **Webhooks**: Webhook receiver endpoints

### Data Routes (`/data/*`)
- **Generation**: Create test data (names, emails, numbers, etc.)
- **Transformation**: Modify data (hash, encode, reverse, etc.)
- **Validation**: Check data against rules
- **Aggregation**: Mathematical operations (sum, average, etc.)
- **Filtering**: Filter data with various criteria
- **Format conversion**: JSON↔CSV↔XML, flatten/unflatten

### Testing Routes (`/simulate/*`, `/stress/*`)
- **Simulation**: Slow responses, random failures, rate limiting
- **Authentication**: Auth testing scenarios
- **Circuit breaker**: Resilience pattern testing
- **Stress testing**: CPU, memory, connection load tests
- **Cascade testing**: Deep call stack testing

### Utility Routes (`/util/*`, `/generate/*`)
- **Health & Status**: Service health checks, version info
- **Connectivity**: Ping, echo endpoints
- **Encoding**: Base64, URL, hex encoding/decoding
- **Hashing**: MD5, SHA1, SHA256, etc.
- **JSON utilities**: Validation, regex testing
- **Fake data generation**: Users, products, transactions, events
- **Time utilities**: Timestamps, format conversion

### Advanced Routes (`/advanced/*`, `/realtime/*`)
- **Streaming**: Chunked responses, Server-Sent Events
- **Pagination**: Complete pagination with navigation
- **GraphQL**: GraphQL simulation
- **Validation**: Complex multi-field validation
- **Nested resources**: Parent-child resource operations
- **Bulk operations**: Process multiple items
- **Real-time**: Live data feeds, notifications, chat simulation
- **Conditional responses**: Different output formats

## Total Endpoints

This structure provides **80+ unique API endpoints** across multiple categories, giving you comprehensive coverage for testing API tools and services.

## Blueprint Registration

All routes are organized as Flask blueprints and can be imported from their respective packages:

```python
from httpbin.routes import api_bp, data_bp, sim_bp, util_bp, advanced_bp
from httpbin.routes.testing.scenarios import stress_bp
from httpbin.routes.advanced.streaming import realtime_bp
from httpbin.routes.data.formats import converters_bp
from httpbin.routes.utils.generators import fake_data_bp
```
