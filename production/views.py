from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic import ListView, DetailView
from django.db.models.deletion import ProtectedError
from django.contrib import messages
from .constants import Unit, UNIT_TO_KG
from django.db.models import *
from accounts.mixins import AdminRequiredMixin, ProducerRequiredMixin

# from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from inventory.models import Ingredient
from .models import *
from .forms import *

# Create your views here.
class CreateFormulaView(AdminRequiredMixin, CreateView):
    model = Formula
    form_class= FormulaForm
    template_name = 'production/formula_create.html'

    def test_func(self):
        return self.request.user.user_type in ['admin', 'producer' ]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formulas'] = Formula.objects.order_by('-updated_at')
        if self.request.POST:
            context['ingredient_formset']= FormulaIngredientFormSet(self.request.POST)
        else:
            context['ingredient_formset']= FormulaIngredientFormSet()
        return context
    
    def get_success_url(self):
        return reverse('production:formula-detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        context = self.get_context_data()
        ingredient_formset = context['ingredient_formset']
        if ingredient_formset.is_valid():
            self.object = form.save(commit=False)
            self.object.created_by = self.request.user
            self.object.save()
            ingredients= ingredient_formset.save(commit=False)
            for ingredient in ingredients:
                ingredient.formula = self.object
                ingredient.save()
            return redirect(self.get_success_url())
        return self.render_to_response(self.get_context_data(form = form))


class FormulaDetailView(AdminRequiredMixin, DetailView):
    model = Formula
    template_name = 'production/formula_detail.html'
    context_object_name = 'formula'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = self.object.ingredients.select_related('ingredient')  # Get related FormulaItem objects
        return context
    

# Formula delete view from formula createlist
class FormulaDeleteView(AdminRequiredMixin, DeleteView):
    model = Formula
    template_name = 'production/formula_delete.html'
    success_url = reverse_lazy('production:formula-create')


class FormulaIngredientDelete(AdminRequiredMixin, DeleteView):
    model = FormulaIngredient
    template_name= 'production/for_ing_delete.html'
    success_message = "Igredient removed from formula successfully"

    def get_object(self, queryset = None):
        formula_id = self.kwargs['formula_id']
        pk = self.kwargs['pk']
        return get_object_or_404(FormulaIngredient, pk=pk, formula__pk = formula_id)

    def get_success_url(self):
        formula_id = self.kwargs.get('formula_id')
        return reverse_lazy('production:formula-detail', kwargs={'pk': formula_id})
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            return super().delete(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, "Cannot delete this formula because it is used in a production batch.")
            return redirect(self.success_url)



class ProductionView(ProducerRequiredMixin, CreateView):
    model = ProductionBatch
    template_name= 'production/production.html'
    success_url= reverse_lazy('production/production_view/')
    fields=['formula', 'unit', 'batch_size', 'notes']

    def get_success_url(self):
        return reverse('production:production-detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['productions']= ProductionBatch.objects.order_by('-production_date')
        if self.request.POST:
            context['prod_form']= ProductionBatchForm(self.request.POST)
        else:
            context['prod_form']= ProductionBatchForm()
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        prod_form = context['prod_form']
        if prod_form.is_valid():
            self.object = prod_form.save(commit=False)
            self.object.produced_by = self.request.user
            self.object.save()
        return redirect(self.get_success_url())



class ProductionDetailView(ProducerRequiredMixin, DetailView):
    model=ProductionBatch
    template_name = 'production/production_detail.html'
    context_object_name='production'
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        ingredients = self.object.formula.ingredients.select_related('ingredient')
        # Aggregare percentage
        total_percentage = self.object.formula.ingredients.aggregate(
            Sum('percentage')
        )['percentage__sum'] or 0
        # print(f'Total Ingredient Percentage : {total_percentage}')

        #Total consumed stock

        #calculate the consumed quantity
        total_consumed =0
        ingredients_with_quantity =[]
        batch_size_kg = self.object.batch_size * UNIT_TO_KG[self.object.unit]
        for i in ingredients:
            if i.ingredient.unit == Unit.TONNES:
                i.ingredient.unit = Unit.KILOGRAMS
                print(f'Unit: {i.ingredient.unit}')
                return i.ingredient.unit
            ingredient_quantity_kg = (i.percentage/100) * batch_size_kg
            # All three quantity returns in Kilograms
            current_quantity_kg = i.ingredient.current_stock * UNIT_TO_KG[i.ingredient.unit]
            previous_stock_kg = i.ingredient.previous_stock * UNIT_TO_KG[i.ingredient.unit]
            total_consumed += ingredient_quantity_kg
            ingredients_with_quantity.append({
                'ingredient': i.ingredient.name,
                'percentage': i.percentage,
                'unit': i.ingredient.unit,
                'previous_stock': previous_stock_kg,
                'consumed_quantity': ingredient_quantity_kg,
                'current_stock': current_quantity_kg
            })
        context['ingredients'] = ingredients_with_quantity
        context['total_percentage']=total_percentage
        context['total_consumed'] = total_consumed
        return context