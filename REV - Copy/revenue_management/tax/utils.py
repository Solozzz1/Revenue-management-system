# utils.py
from django.core.exceptions import PermissionDenied

def is_admin(user):
    return user.is_authenticated and user.userprofile.role == 'admin'

def is_auditor(user):
    return user.is_authenticated and user.userprofile.role == 'auditor'

def is_taxpayer(user):
    return user.is_authenticated and user.userprofile.role == 'taxpayer'

def role_required(role):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            if not getattr(request.user.userprofile, 'role', None) == role:
                raise PermissionDenied
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
