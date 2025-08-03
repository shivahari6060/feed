from django.db import models

class Role(models.TextChoices):
    ADMIN = 'admin', 'Admin'
    INVENTORY = 'inventory', 'Inventory Manager'
    PRODUCTION = 'production', 'Production Manager'
