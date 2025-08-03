from django.db import models
from decimal import Decimal

class Unit(models.TextChoices):
    GRAMS = 'g', 'Grams'
    KILOGRAMS = 'kg', 'Kilograms'
    TONNES = 't', 'Tonnes'


#Conversion factors to kilograms (which is here base unit)
UNIT_TO_KG ={
    Unit.GRAMS: Decimal ('0.001'),
    Unit.KILOGRAMS: Decimal ('1'),
    Unit.TONNES: Decimal ('1000'),
}