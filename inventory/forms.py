from django.forms import ModelForm
from .models import *

class IngredientForm(ModelForm):
    class Meta:
        model = Ingredient
        fields =['name', 'description', 'unit', 'cost_per_unit', 'added_stock', 'min_threshold']

class IngredientUpdateForm(ModelForm):
    class Meta:
        model=StockUpdate
        fields = ['ingredient', 'quantity', 'note']