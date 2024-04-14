import random
from flask import redirect, session
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("userId") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def issueNewCard():
    cardNum = str(random.randint(10**13,(10**14)-1))
    accountNum = str(random.randint(10**13,(10**14)-1))
    cvvNum = str(random.randint(100,999))
    return {
        'cardNumber':cardNum, 
        'cvvNumber': cvvNum,
        'accountNumber': accountNum
    }
        
