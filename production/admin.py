from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Formula)
admin.site.register(FormulaIngredient)
admin.site.register(ProductionBatch)