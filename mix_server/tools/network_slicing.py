import requests
from utils.api_definitions import OpenAPIAnalyzer
from server import mcp
from utils.api_definitions import load_openapi_with_refs, get_request_schema

# @mcp.tool()
# def build_slice_request(request: str) -> str:
#     """
#     Parse natural language request and validate it against the NetworkSliceBooking API spec
#     """
#     structured_data = interpret_natural_language(request)
#     return structured_data


@mcp.tool()
def load_openapi_spec(method: str = "POST") -> str:
    """
    Load OpenAPI spec from YAML file and return an analyzer instance
    """
    analyzer = OpenAPIAnalyzer("/Users/kim/Documents/GitHub/mcp-camara-demo/mix_server/utils/NetworkSliceBooking.yaml", method)
    
    return analyzer.openapi_doc



@mcp.tool()
# calls to an api in the path /sessions in localhost:9000
def call_sessions_api(payload: dict) -> dict:
    """
    Send a POST request to /sessions on localhost:9000 with the given payload.
    Returns the JSON response as a dict.
    """
    url = "http://localhost:9000/sessions"
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"API call failed: {e}")
        return {"error": str(e)}

#def interpret_natural_language(text: str, yaml_file: str, api_path: str, method: str = "POST") -> dict:
def interpret_natural_language(text: str, method: str = "POST") -> dict:
    """
    Analyze text against OpenAPI spec from YAML file
    Returns analysis results and suggestions
    """
    analyzer = OpenAPIAnalyzer("/Users/kim/Documents/GitHub/mcp-camara-demo/mix_server/utils/NetworkSliceBooking.yaml",method)
    result = analyzer.analyze_text(text)
    
    print(f"Schema properties: {result['schema_properties']}")
    print(f"Found parameters: {list(result['found_parameters'].keys())}")
    print(f"Missing required: {result['missing_required']}")
    print(f"Ready to call API: {result['ready_to_call']}")
    
    return result['suggested_api_call']


