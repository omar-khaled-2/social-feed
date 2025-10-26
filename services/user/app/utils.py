from flask import request
from functools import wraps
from app.config import Config


def api_token_required():

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            api_token = request.headers.get("Authorization", "")
            if not api_token:
                raise "Authorization header is missing"
            

        
            if not api_token in Config.ALLOWED_API_TOKENS:
                raise "API token is invalid"

      
            return f(*args, **kwargs)

        return wrapper
    return decorator