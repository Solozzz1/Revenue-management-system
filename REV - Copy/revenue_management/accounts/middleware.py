from django.shortcuts import redirect
from django.urls import reverse
from django.core.exceptions import PermissionDenied

def role_required(allowed_roles):
    def decorator(view_func):
        def wrap(request, *args, **kwargs):
            if request.user.is_authenticated and request.user.roles.filter(name__in=allowed_roles).exists():
                return view_func(request, *args, **kwargs)
            else:
                raise PermissionDenied
        return wrap
    return decorator