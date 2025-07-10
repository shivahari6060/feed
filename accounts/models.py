from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES=(
        ('admin', 'Admin'),
        ('inventory', 'Inventory Manager'),
        ('producer', 'Feed Producer'),
    )
    user_type= models.CharField(max_length=20, choices=USER_TYPE_CHOICES)

    groups = models.ManyToManyField(Group, related_name='custom_user_set')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_set')