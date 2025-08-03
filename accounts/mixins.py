# mixins.py
from django.core.exceptions import PermissionDenied
from .models import *
from .constants import *

class RoleRequiredMixin:
    required_roles = []

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.user_type not in self.required_roles:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

class AdminRequiredMixin(RoleRequiredMixin):
    required_roles = [Role.ADMIN]

class InventoryRequiredMixin(RoleRequiredMixin):
    required_roles = [Role.ADMIN, Role.INVENTORY]


class ProducerRequiredMixin(RoleRequiredMixin):
    required_roles= [Role.ADMIN, Role.PRODUCTION]



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