from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

class Alert(models.Model):
    ALERT_TYPES = (
        ('low_stock', 'Low Stock'),
        ('production', 'Production Alert'),
        ('system', 'System Notification')
    )
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPES)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    recipient = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    related_object_id = models.PositiveIntegerField(null=True) # For linking to ingredient/production
    