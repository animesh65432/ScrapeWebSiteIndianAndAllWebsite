from typing import Dict, Any

def validate_translation(data: Dict[str, Any], target_language: str) -> None:
    """
    Validate that translation data has all required fields.
    
    Raises:
        ValueError: If validation fails
    """
    required_fields = ["title", "content", "description", "state"]
    missing = [field for field in required_fields if field not in data or not data[field]]
    
    if missing:
        raise ValueError(f"Missing or empty required fields: {', '.join(missing)}")
    
    for field in ["title", "content", "description", "state"]:
        value = data[field]
        if not isinstance(value, str):
            raise ValueError(f"Field '{field}' must be a string, got {type(value)}")
        if len(value.strip()) == 0:
            raise ValueError(f"Field '{field}' cannot be empty")