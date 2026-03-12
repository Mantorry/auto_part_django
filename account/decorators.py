from functools import wraps
from django.shortcuts import redirect


def login_required_custom(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('user_id'):
            return redirect('account:login')
        return view_func(request, *args, **kwargs)
    return wrapper


def role_required(*roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.session.get('user_id'):
                return redirect('account:login')
            if request.session.get('user_role') not in roles and not request.session.get('is_superuser'):
                return redirect('catalog:index')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
