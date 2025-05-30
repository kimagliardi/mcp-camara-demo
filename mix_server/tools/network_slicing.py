from utils.api_definitions import OpenAPIAnalyzer
from server import mcp
from utils.api_definitions import load_openapi_with_refs, get_request_schema

@mcp.tool()
def build_slice_request(request: str) -> str:
    """
    Parse natural language request and validate it against the NetworkSliceBooking API spec
    """
    structured_data = interpret_natural_language(request)
    openapi_file = "NetworkSliceBooking.yaml"
    try:
        openapi_doc = load_openapi_with_refs(openapi_file)
        schema = get_request_schema(openapi_doc, "/sessions", "post")
    except Exception as e:
        return f"⚠️ Failed to load API schema: {e}"

    return structured_data

def interpret_natural_language(text: str, yaml_file: str, api_path: str, method: str = "POST") -> dict:
    """
    Analyze text against OpenAPI spec from YAML file
    Returns analysis results and suggestions
    """
    analyzer = OpenAPIAnalyzer(yaml_file, api_path, method)
    result = analyzer.analyze_text(text)
    
    print(f"Schema properties: {result['schema_properties']}")
    print(f"Found parameters: {list(result['found_parameters'].keys())}")
    print(f"Missing required: {result['missing_required']}")
    print(f"Ready to call API: {result['ready_to_call']}")
    
    return result['suggested_api_call']
