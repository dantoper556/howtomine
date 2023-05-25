from typing import Any, Mapping, Optional, Type, Union
from django.forms import *
from django.forms.utils import ErrorList
from .models import *

class ElectricityPriceForm(Form):
    val = IntegerField(label="electricity price in usd, $/kWh")

class ChooseCardForm(Form):
    # electricity = DecimalField(label="electricity price in usd", min_value=0, required=True)
    cnt = IntegerField(required=False, label="", widget=HiddenInput())
    cards = ChoiceField(label="", choices=((i, VideoCard.objects.all()[i].name) for i in range(len(VideoCard.objects.all()))))
    quantity = IntegerField(required=True, label="", min_value=1)
