from flask import jsonify
from typing import Any, Dict, Optional

def api_response(
    data: Dict[str, Any] = None,
    message: str = "",
    status: str = "success",
    status_code: int = 200
) -> Any:
    """Standard API response format"""
    response_data = {
        "status": status,
        "message": message,
        "data": data or {}
    }
    response = jsonify(response_data)
    response.status_code = status_code
    return response