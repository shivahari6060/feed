from django.forms import ModelForm
from .models import Ingredient

class IngredientForm(ModelForm):
    class Meta:
        model = Ingredient
        fields =['name', 'description', 'unit', 'cost_per_unit','current_stock', 'min_threshold']
