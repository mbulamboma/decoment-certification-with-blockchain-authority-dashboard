from flask import session, request, redirect, url_for
from functools import wraps

def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        # Check if the 'loggedin' key exists in session and is True
        if 'loggedin' in session and session.get('loggedin') is True:
            return func(*args, **kwargs)
        else:
            # If not logged in, redirect to the '/login' URL with 'next' parameter
            next_url = request.url
            return redirect(url_for('login', next=next_url))
    return decorated_function

def redirect_cpanel_if_loggedIn(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        # Check if the 'loggedin' key exists in session and is True
        if 'loggedin' in session and  session.get('loggedin') is True:
            return redirect(url_for('cpanel'))
        else:
            return func(*args, **kwargs) 
    return decorated_function