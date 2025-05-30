import re
import yaml
import jsonref
from typing import Dict, List, Any, Optional

class OpenAPIAnalyzer:
    def __init__(self, yaml_file_path: str, api_path: str, method: str = "POST"):
        self.openapi_doc = self.load_openapi_with_refs("NetworkSliceBooking.yaml")
        self.api_path = api_path
        self.method = method.lower()
        self.schema = self.get_request_schema()
        
    def load_openapi_with_refs(self, file_path: str):
        with open(file_path, 'r') as f:
            spec = yaml.safe_load(f)
            return jsonref.JsonRef.replace_refs(spec)

    def get_request_schema(self):
        return self.openapi_doc["paths"][self.api_path][self.method]["requestBody"]["content"]["application/json"]["schema"]
    
    def get_required_fields(self) -> List[str]:
        """Extract required fields from OpenAPI schema"""
        return self.schema.get("required", [])
    
    def get_all_properties(self) -> Dict[str, Any]:
        """Get all properties from the schema"""
        return self.schema.get("properties", {})
    
    def analyze_text(self, text: str) -> Dict[str, Any]:
        """Main function: analyze text against OpenAPI schema"""
        
        # Get schema info
        required_fields = self.get_required_fields()
        all_properties = self.get_all_properties()
        
        found_params = self._extract_params(text, all_properties)
        
        # Check what's missing
        missing_required = []
        for field in required_fields:
            if field not in found_params:
                missing_required.append(field)
        
        # Build suggested API call with defaults/examples from schema
        suggested_call = self._build_suggested_call(found_params, all_properties)
        
        return {
            "found_parameters": found_params,
            "missing_required": missing_required,
            "all_required_fields": required_fields,
            "suggested_api_call": suggested_call,
            "ready_to_call": len(missing_required) == 0,
            "schema_properties": list(all_properties.keys())
        }

    def _extract_params(self, text: str, properties: Dict[str, Any]) -> Dict[str, Any]:
        """Extract parameters based on property names and common patterns"""
        params = {}
        text_lower = text.lower()
        
        # Check each property in the schema
        for prop_name, prop_schema in properties.items():
            prop_lower = prop_name.lower()
            
            # Direct property name match
            if prop_lower in text_lower:
                params[prop_name] = self._extract_value_for_property(text, prop_name, prop_schema)
                continue
            
            # Common patterns based on property types
            prop_type = prop_schema.get("type", "")
            
            # Time-related fields
            if any(time_word in prop_lower for time_word in ['time', 'start', 'end', 'duration']):
                if re.search(r'\d{4}-\d{2}-\d{2}', text) or any(word in text_lower for word in ['time', 'when', 'from', 'to', 'start', 'end']):
                    params[prop_name] = "detected_needs_parsing"
            
            # Location/area fields
            elif any(loc_word in prop_lower for loc_word in ['area', 'location', 'position', 'coordinate', 'lat', 'lon']):
                if any(word in text_lower for word in ['lat', 'long', 'coordinate', 'location', 'area', 'radius']):
                    params[prop_name] = "detected_needs_parsing"
            
            # QoS/performance fields
            elif any(qos_word in prop_lower for qos_word in ['qos', 'quality', 'throughput', 'latency', 'bandwidth']):
                if any(word in text_lower for word in ['mbps', 'gbps', 'latency', 'throughput', 'bandwidth', 'ms', 'millisecond']):
                    params[prop_name] = "detected_needs_parsing"
            
            # String fields with quotes
            elif prop_type == "string":
                # Look for quoted strings that might be names/identifiers
                quoted_match = re.search(rf'{prop_lower}["\s]*["\']([^"\']+)["\']', text, re.IGNORECASE)
                if quoted_match:
                    params[prop_name] = quoted_match.group(1)
            
            # Integer/number fields
            elif prop_type in ["integer", "number"]:
                # Look for numbers near this property name
                number_match = re.search(rf'{prop_lower}["\s]*(\d+)', text, re.IGNORECASE)
                if number_match:
                    params[prop_name] = int(number_match.group(1)) if prop_type == "integer" else float(number_match.group(1))
        
        return params
    
    def _extract_value_for_property(self, text: str, prop_name: str, prop_schema: Dict[str, Any]) -> Any:
        """Extract specific value for a detected property"""
        prop_type = prop_schema.get("type", "")
        
        # For now, return a placeholder - you can enhance this
        if prop_type == "string":
            return "detected_string_value"
        elif prop_type == "integer":
            return 0
        elif prop_type == "number":
            return 0.0
        elif prop_type == "object":
            return "detected_object_needs_parsing"
        elif prop_type == "array":
            return "detected_array_needs_parsing"
        else:
            return "detected_value"
    
    def _build_suggested_call(self, found_params: Dict[str, Any], properties: Dict[str, Any]) -> Dict[str, Any]:
        """Build API call using found params + schema examples/defaults"""
        suggested = {}
        
        for prop_name, prop_schema in properties.items():
            if prop_name in found_params:
                # Use what we found (though might need further parsing)
                suggested[prop_name] = found_params[prop_name]
            else:
                # Use example or default from schema, or create placeholder
                if "example" in prop_schema:
                    suggested[prop_name] = prop_schema["example"]
                elif "default" in prop_schema:
                    suggested[prop_name] = prop_schema["default"]
                else:
                    # Create a reasonable placeholder based on type
                    suggested[prop_name] = self._create_placeholder(prop_schema)
        
        return suggested
    
    def _create_placeholder(self, prop_schema: Dict[str, Any]) -> Any:
        """Create placeholder values based on schema type"""
        prop_type = prop_schema.get("type", "")
        
        if prop_type == "string":
            return f"<{prop_schema.get('description', 'string_value')}>"
        elif prop_type == "integer":
            return 0
        elif prop_type == "number":
            return 0.0
        elif prop_type == "boolean":
            return False
        elif prop_type == "array":
            return []
        elif prop_type == "object":
            return {}
        else:
            return None

def load_openapi_with_refs(self, file_path: str):
    with open(file_path, 'r') as f:
        spec = yaml.safe_load(f)
        return jsonref.JsonRef.replace_refs(spec)

def get_request_schema(self):
    return self.openapi_doc["paths"][self.api_path][self.method]["requestBody"]["content"]["application/json"]["schema"]
