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



