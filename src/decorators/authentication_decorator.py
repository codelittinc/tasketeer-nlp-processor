from flask import request, abort
from functools import wraps 
import os

def auth_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
      # if the app is running in development mode, does not apply authentication
      env = os.environ.get('ENV', '')
      if env == "development":
        return f(*args, **kwargs)
               
      api_key_user = request.headers.get("Authorization")
      api_key_app = os.environ.get('AUTHORIZATION', '')
      if not api_key_user or  not api_key_app or api_key_app != api_key_user:
        abort(401)      
  
      # call the function
      return f(*args, **kwargs)  
    return wrap