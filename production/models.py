from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from inventory.models import StockUpdate
from .constants import Unit, UNIT_TO_KG
from django.core.exceptions import ValidationError

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
    formula = models.ForeignKey(Formula,
                                on_delete=models.CASCADE,
                                related_name='ingredients')
    ingredient = models.ForeignKey('inventory.Ingredient',
                                   on_delete=models.CASCADE)
    percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0.01), MaxValueValidator(100)]
    )

    def __str__(self):
        return self.ingredient.name


class ProductionBatch(models.Model):
    formula = models.ForeignKey(Formula, on_delete=models.PROTECT)
    unit = models.CharField(
        max_length=2, choices=Unit.choices, default=Unit.TONNES)
    batch_size = models.DecimalField(
        max_digits=15, decimal_places=2,
        validators=[MinValueValidator(0.1)])
    production_date = models.DateTimeField(auto_now_add=True)
    produced_by = models.ForeignKey('accounts.CustomUser',
                                     on_delete=models.SET_NULL,
                                     null=True)
    notes = models.TextField(blank=True)

    def clean(self):
        #validate stock levels befor saving
        for comp in self.formula.ingredients.all():
            #convert the batch size to kg (common unit)
            batch_size_kg = self.batch_size * UNIT_TO_KG[self.unit]
            # print(UNIT_TO_KG[self.unit])
            quantity_needed_kg = (comp.percentage / 100) * batch_size_kg

            #now convert ingredient stock to kg
            ingredient = comp.ingredient
            stock_kg = ingredient.current_stock * UNIT_TO_KG[ingredient.unit.lower()]

            #validate needed and stock are equal or greater than
            if quantity_needed_kg > stock_kg:
                raise ValidationError(
                    f"Insuffient Stock for {ingredient.name}."
                    f"Needed: {quantity_needed_kg} Kg , Available: {stock_kg} Kg.")
            return quantity_needed_kg
    

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        #update stock levels
        for comp in self.formula.ingredients.all():
            batch_size_kg = self.batch_size * UNIT_TO_KG[self.unit]
            quantity_used_kg = (comp.percentage / 100) * batch_size_kg

            #convert bak to the ingredients original unit for deduction
            ingredient = comp.ingredient
            quantity_used_in_ingredient_unit = quantity_used_kg / UNIT_TO_KG[ingredient.unit.lower()]

            #now update stocks
            StockUpdate.objects.create(
                ingredient= ingredient,
                quantity =- quantity_used_in_ingredient_unit,
                updated_by = self.produced_by,
                note = f'Used in production batch #{self.id}'
            )
    
    def get_ingredients(self):
        return self.formula.ingredients.select_related('ingredient')
    