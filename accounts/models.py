from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser, Group, Permission, PermissionsMixin
from django.db import models
from .constants import *

class CustomUser(AbstractUser, PermissionsMixin):
    user_type= models.CharField(max_length=10, choices=Role.choices, default=Role.INVENTORY)
    role_issue = models.BooleanField(default=False)

    groups = models.ManyToManyField(Group, related_name='custom_user_set')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_set')