from django.urls import path
from .views import *

app_name = 'inventory' # This name important for reverse lookup


urlpatterns = [
    path('list/', InventoryView.as_view(), name='inventory-list'),
    path('ingredient/update/<int:pk>/', IngredientUpdateView.as_view(), name='ingredient-update'),
    path('ingredient/delete/<int:pk>/', IngredientDeleteView.as_view(), name='ingredient-delete'),
    path('search/', search_ingredient, name="ingredient-search"),
]