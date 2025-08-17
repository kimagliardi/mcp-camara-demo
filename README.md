# MCP CAMARA Demo - Mix Server

A Model Context Protocol (MCP) server that provides tools for interacting with CAMARA Network Slice Booking APIs through natural language processing.

## Overview

This project demonstrates how to create an MCP server that can:
- Parse natural language requests for network slice bookings
- Validate requests against OpenAPI specifications
- Make API calls to CAMARA-compliant network slicing services
- Analyze and extract parameters from text descriptions

## Features

- **OpenAPI Integration**: Load and analyze CAMARA Network Slice Booking API specifications
- **Natural Language Processing**: Extract network slicing parameters from text descriptions
- **API Validation**: Validate requests against OpenAPI schemas before making calls
- **MCP Tools**: Expose functionality through Model Context Protocol tools

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/kimagliardi/mcp-camara-demo.git
   cd mcp-camara-demo/mix_server
   ```

2. **Install dependencies**:
   ```bash
   uv install
   ```

   Or with pip:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the MCP Server

```bash
python main.py
```

### Available MCP Tools

#### 1. `load_openapi_spec(method: str = "POST")`
Load the OpenAPI specification from the NetworkSliceBooking.yaml file.

**Parameters:**
- `method`: HTTP method (default: "POST")

**Returns:** OpenAPI document structure

#### 2. `call_sessions_api(payload: dict)`
Send a POST request to the `/sessions` endpoint on localhost:9000.

**Parameters:**
- `payload`: JSON payload for the API call

**Returns:** API response as a dictionary

#### 3. `interpret_natural_language(text: str, method: str = "POST")`
Analyze natural language text against the OpenAPI schema and extract network slicing parameters.

**Parameters:**
- `text`: Natural language description of network slice requirements
- `method`: HTTP method (default: "POST")

**Returns:** Suggested API call structure

## Project Structure

```
mix_server/
├── main.py                 # Entry point
├── server.py              # MCP server configuration
├── pyproject.toml         # Project dependencies
├── tools/
│   ├── network_slicing.py # Network slicing MCP tools
│   └── NetworkSliceBooking.yaml # CAMARA API spec (copy)
└── utils/
    ├── api_definitions.py # OpenAPI analysis utilities
    └── NetworkSliceBooking.yaml # CAMARA API specification
```

## API Analysis Features

The `OpenAPIAnalyzer` class provides comprehensive analysis of CAMARA API specifications:

- **Schema Validation**: Extract required fields and property definitions
- **Parameter Extraction**: Identify network slicing parameters from natural language
- **API Path Discovery**: Load and analyze all available API endpoints
- **Request Building**: Generate valid API requests from extracted parameters

### Example Usage

```python
from utils.api_definitions import OpenAPIAnalyzer

# Initialize analyzer with CAMARA spec
analyzer = OpenAPIAnalyzer("utils/NetworkSliceBooking.yaml")

# Analyze natural language text
result = analyzer.analyze_text("I need a network slice with 100 Mbps throughput")

# Get API summary
summary = analyzer.describe_api()
print(summary)
```

## CAMARA Integration

This project is designed to work with CAMARA Network Slice Booking APIs, which provide standardized interfaces for:

- Network slice creation and management
- Quality of Service (QoS) configuration
- Geographic area specification
- Throughput and latency requirements

## Development

### Adding New Tools

1. Create new tool functions in `tools/network_slicing.py`
2. Decorate with `@mcp.tool()`
3. Import the module in `main.py`

### Extending API Analysis

The `OpenAPIAnalyzer` class can be extended to support additional CAMARA APIs by:
- Adding new parameter extraction patterns
- Supporting additional OpenAPI schema features
- Implementing custom validation rules

## Dependencies

- **mcp[cli]**: Model Context Protocol implementation
- **PyYAML**: YAML file parsing
- **jsonref**: JSON reference resolution
- **jsonschema**: JSON schema validation
- **requests**: HTTP API calls
- **openapi-spec-validator**: OpenAPI specification validation


## Related Projects

- [CAMARA Project](https://camaraproject.org/)
- [Network Slice Booking API](https://github.com/camaraproject/NetworkSlicing)
- [Model Context Protocol](https://modelcontextprotocol.io/)