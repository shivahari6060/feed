from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.contrib import messages

from django.views.generic.edit import FormView
from django.views.generic import UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Ingredient
from .forms import IngredientForm

class InventoryView(LoginRequiredMixin, FormView):
    template_name = 'inventory/inventory_dash.html'
    form_class = IngredientForm
    success_url = reverse_lazy('inventory:inventory-list')  # make sure this URL name exists

    def form_valid(self, form):
        ingredient = form.save(commit=False)
        ingredient.created_by = self.request.user
        ingredient.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ingredients'] = Ingredient.objects.order_by('name')
        context['re_ingredients'] = Ingredient.objects.order_by('-created_at')
        context['low_stock'] = Ingredient.objects.filter(
            current_stock__lt=F('min_threshold')
        )
        return context
    

# Add to existing views.py
class IngredientUpdateView(LoginRequiredMixin, UpdateView):
    model = Ingredient
    form_class = IngredientForm
    template_name = 'inventory/invt_update.html'
    success_url = reverse_lazy('inventory:inventory-list')

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)
    

def search_ingredient(request):
    query = request.GET.get('q', '') #get query from url
    form = IngredientForm()
    re_ingredients = Ingredient.objects.order_by('-created_at')
    if query:
        ingredients = Ingredient.objects.filter(name__icontains=query)
    else:
        ingredients = Ingredient.objects.all()
    context ={
        'ingredients':ingredients,
        'query':query, 
        'form':form,
        're_ingredients': re_ingredients
    }
    return render(request, 'inventory/inventory_dash.html', context=context)

