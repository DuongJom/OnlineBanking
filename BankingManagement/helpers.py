from flask import redirect, session
from functools import wraps


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("userId") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def list_to_json(objList):
        objs = []
        if objList is not None:
            for obj in objList:
                objs.append(obj.to_json())
        return objs

