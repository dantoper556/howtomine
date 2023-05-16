from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from .forms import *

def main_page(request):
    return render(request, 'main_page.html')

def make_conf_page(request):
    return render(request, 'make_conf_page.html')

def calc_profit_page(request):
    b = 0
    data = dict()
    data["cards"] = []
    for obj in VideoCard.objects.all():
        data["cards"].append(obj.name)

    data["was"] = 0
    data["form"] = ChooseCardForm()
    if (request.method == "POST"):
        form = ChooseCardForm(request.POST)
        if (form.is_valid()):
            data["was"] = 1
            data["chosen_card"] = VideoCard.objects.all()[int(form.cleaned_data["cards"])]
        else:
            return HttpResponse("not hooray")
        # return render(request, 'calc_profit_page.html', context={"cards": ['testik']})
    return render(request, 'calc_profit_page.html', context=data)
