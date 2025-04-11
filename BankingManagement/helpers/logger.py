import logging
import os
from datetime import datetime
from functools import wraps
from flask import request, g, Response

# Create logs directory if it doesn't exist
if not os.path.exists('logs'):
    os.makedirs('logs')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'logs/app_{datetime.now().strftime("%Y%m%d")}.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('banking_app')

def log_request():
    """Decorator to log request details"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Log request details
            request_id = g.get('request_id', 'N/A')
            logger.info(f"Request ID: {request_id}")
            logger.info(f"Method: {request.method}")
            logger.info(f"Path: {request.path}")
            logger.info(f"IP: {request.remote_addr}")
            
            if request.is_json:
                logger.info(f"JSON Data: {request.get_json()}")
            elif request.form:
                logger.info(f"Form Data: {dict(request.form)}")
            
            # Execute the route function
            response = f(*args, **kwargs)
            
            # Log response status
            if isinstance(response, Response):
                logger.info(f"Response Status: {response.status_code}")
            else:
                logger.info("Response: String or other type returned")
            
            return response
        return decorated_function
    return decorator 