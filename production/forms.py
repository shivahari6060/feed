from django.forms import ModelForm
from django import forms
from .models import *
from inventory.models import Ingredient

class FormulaForm(ModelForm):
    class Meta:
        model = Formula
        fields=['name', 'description']
        labels ={
            'name': 'Name of the Formula',
            'description': 'Description About Formula'
        }


class FormulaIngredientForm(ModelForm):
    class Meta:
        model = FormulaIngredient
        fields =['formula','ingredient', 'percentage']

#creating Formula Ingredient Formset
FormulaIngredientFormSet = forms.inlineformset_factory(
    Formula,
    FormulaIngredient,
    form=FormulaIngredientForm,
    extra=60,  # Show 5 empty ingredient slots by default
    can_delete=False,
    min_num=1,  # At least one ingredient required
    validate_min=True,
    max_num=60,  # Maximum ingredients per formulation
    validate_max=True,
)

class ProductionBatchForm(ModelForm):
    class Meta:
        model=ProductionBatch
        fields=['formula', 'unit', 'batch_size', 'notes']
        labels={
            'unit': "Select Production Unit"
        }
