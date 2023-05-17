from typing import Any, Mapping, Optional, Type, Union
from django.forms import *
from django.forms.utils import ErrorList
from .models import *

class ChooseCardForm(Form):
    cnt = IntegerField(required=False, label="", widget=HiddenInput())
    cards = ChoiceField(label="", choices=((i, VideoCard.objects.all()[i].name) for i in range(len(VideoCard.objects.all()))))
    quantity = IntegerField(required=True, label="", min_value=1)
