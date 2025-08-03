from django.db import models
from django.core.validators import MinValueValidator
from production.constants import Unit, UNIT_TO_KG

# Create your models here.

class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True) # this sets all different ingredient is used
    description = models.TextField(blank=True)
    unit = models.CharField(max_length=2,
                            choices=Unit.choices,
                            default=Unit.KILOGRAMS)
    previous_stock = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    current_stock = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    added_stock = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    min_threshold = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cost_per_unit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_by = models.ForeignKey('accounts.CustomUser', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name   

class StockUpdate(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0.01)])
    timestamp = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey('accounts.CustomUser', on_delete=models.SET_NULL, null=True)
    note = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        #update current stock
        self.ingredient.current_stock += self.quantity
        self.ingredient.save()
