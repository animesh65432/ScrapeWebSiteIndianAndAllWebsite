import json
import re
from typing import Any, Dict

def clean_json_response(raw: str) -> str:
    """Remove markdown code blocks and extra whitespace."""
    raw = re.sub(r'^```(?:json)?\s*', '', raw, flags=re.MULTILINE)
    raw = re.sub(r'```\s*$', '', raw, flags=re.MULTILINE)
    return raw.strip()


def repair_json_string(json_str: str) -> str:
    """
    Attempt to fix common JSON formatting issues from LLM responses.
    Handles unescaped newlines and quotes within string values.
    """
    # Track if we're inside a string value
    result = []
    i = 0
    in_string = False
    
    while i < len(json_str):
        char = json_str[i]
        
        # Check if we're entering/exiting a string
        if char == '"' and (i == 0 or json_str[i-1] != '\\'):
            in_string = not in_string
            result.append(char)
        elif in_string:
            # Inside a string - escape special characters
            if char == '\n':
                result.append('\\n')
            elif char == '\r':
                result.append('\\r')
            elif char == '\t':
                result.append('\\t')
            else:
                result.append(char)
        else:
            # Outside string - keep as is
            result.append(char)
        
        i += 1
    
    return ''.join(result)


def safe_parse_json(raw: str, context: str = "") -> Dict[str, Any]:
    cleaned = clean_json_response(raw)
    
    # Step 2: Try direct parsing
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as first_error:
        print(f"⚠️ JSON parse failed ({context}): {first_error.msg}")
        
        # Step 3: Try repairing common issues
        try:
            repaired = repair_json_string(cleaned)
            return json.loads(repaired)
        except json.JSONDecodeError as second_error:
            # Step 4: All attempts failed
            error_msg = (
                f"Failed to parse JSON after repair attempts.\n"
                f"Context: {context}\n"
                f"Error: {second_error.msg} at line {second_error.lineno}, col {second_error.colno}\n"
                f"Raw response preview (first 300 chars):\n{raw[:300]}"
            )
            print(f"❌ {error_msg}")
            raise ValueError(error_msg)