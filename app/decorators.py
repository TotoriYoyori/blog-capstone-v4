from functools import wraps
from flask import abort
from flask_login import current_user
from .models import Domain


def permission_required(domain: str):
    def decorator(func):
        # This ensures that the origin func name is still valid for routing (url_for(og_func)) otherwise it will be
        ## be wrapper (or decorated_function) in this case.
        @wraps(func)
        def decorated_function(*args, **kwargs):
            if domain not in current_user.email:
                abort(403)

            return func(*args, **kwargs)
        return decorated_function
    return decorator


def admin_required(func):
    return permission_required(Domain.ADMIN)(func)
