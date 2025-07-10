from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Ingredient
from notifications.models import Alert

@receiver(post_save, sender=Ingredient)
def check_stock_level(sender, instance, **kwargs):
    if instance.current_stock < instance.min_threshold:
        #create alert for inventory managers
        inventory_managers = sender.objects.filter(user_type='inventory')
        for manager in inventory_managers:
            Alert.objects.create(
                alert_type = 'low stock',
                message = f'{instance.name} stock is low ({instance.current_stock} {instance.unit} remaining)',
                recipient = manager,
                related_object_id = instance.id
            )