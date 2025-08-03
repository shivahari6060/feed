from django.core.exceptions import PermissionDenied
from functools import wraps
from .constants import Role

def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.user_type != Role.ADMIN:
            raise PermissionDenied()
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def inventory_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.user_type not in [Role.ADMIN, Role.INVENTORY]:
            raise PermissionDenied()
        return view_func(request, *args, **kwargs)
    return _wrapped_view