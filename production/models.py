from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from inventory.models import StockUpdate

# Create your models here.

class Formula(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey('accounts.CustomUser', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class FormulaIngredient(models.Model):
    formula = models.ForeignKey(Formula, on_delete=models.CASCADE, related_name='ingredients')
    ingredient = models.ForeignKey('inventory.Ingredient', on_delete=models.CASCADE, related_name='ingredients')
    percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0.01), MaxValueValidator(100)]
    )

    def __str__(self):
        return self.ingredient.name


class ProductionBatch(models.Model):
    formula = models.ForeignKey(Formula, on_delete=models.PROTECT)
    unit = models.CharField(max_length=10) # kg, gm, tonne, replace with choices
    batch_size = models.DecimalField(max_digits=15, decimal_places=2,
                                     validators=[MinValueValidator(0.1)])
    production_date = models.DateTimeField(auto_now_add=True)
    produced_by = models.ForeignKey('accounts.CustomUser', on_delete=models.SET_NULL, null=True)
    notes = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        #update stock levels
        for comp in self.formula.ingredients.all():
            quantity_used = (comp.percentage / 100) * self.batch_size
            StockUpdate.objects.create(
                ingredient= comp.ingredient,
                quantity =- quantity_used,
                updated_by = self.produced_by,
                note = f'Used in production batch #{self.id}'
            )
    