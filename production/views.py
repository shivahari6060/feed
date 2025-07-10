from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic import ListView, DetailView
# from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from .models import *
from .forms import *

# Create your views here.
class CreateFormulaView( CreateView):
    model = Formula
    form_class= FormulaForm
    template_name = 'production/formula_create.html'
    # success_url= reverse_lazy(reverse('production:formula-detail', kwargs={'pk': self.object.pk}))

    def test_func(self):
        return self.request.user.user_type in ['admin', 'producer' ]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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


class FormulaDetailView(DetailView):
    model = Formula
    template_name = 'production/formula_detail.html'
    context_object_name = 'formula'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = self.object.ingredients.select_related('ingredient')  # Get related FormulaItem objects
        return context

class ProductionView(CreateView):
    model = ProductionBatch
    template_name= 'production/production.html'
    success_url= reverse_lazy('production/production-list')
    fields=['formula', 'unit', 'batch_size', 'notes']

    def get_success_url(self):
        return reverse('production:production-detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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

class ProductionListView(ListView):
    model=ProductionBatch
    template_name = 'production/production_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['productions']= ProductionBatch.objects.order_by('-production_date')
        return context

class ProductionDetailView(DetailView):
    model=ProductionBatch
    template_name = 'production/production_detail.html'