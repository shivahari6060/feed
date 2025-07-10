from django.urls import path
from .views import *

app_name = 'production' # This name important for reverse lookup


urlpatterns = [
    path('formula_create/', CreateFormulaView.as_view(), name='formula-create'),
    path('formula_detail/<int:pk>/', FormulaDetailView.as_view(), name='formula-detail'),
    path('production_view/', ProductionView.as_view(), name='production'),
    path('production_list/', ProductionListView.as_view(), name='production-list'),
    path('production/detail/<int:pk>/', ProductionDetailView.as_view(), name='production-detail'),
    # path('register/', views.register_view, name='register'),
]