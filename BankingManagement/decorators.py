from functools import wraps
from flask import Response, g, redirect, flash, request, session
from models import database
from enums.collection import CollectionType
from message import messages_failure
from helpers.logger import logger

db = database.Database().get_db()
accounts = db[CollectionType.ACCOUNTS.value]

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("account_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def role_required(*roles):
    """
    Decorator to check if the current user has the required role(s)
    Usage: @role_required(RoleType.ADMIN.value, RoleType.EMPLOYEE.value)
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not session.get("account_id"):
                return redirect("/login")
                
            current_account = accounts.find_one({"_id": int(session.get("account_id"))})
            if not current_account:
                session.clear()
                return redirect("/login")
                
            if current_account["Role"] not in roles:
                flash(messages_failure["unauthorized_access"], "error")
                return redirect("/")
                
            return f(*args, **kwargs)
        return decorated_function
    return decorator

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