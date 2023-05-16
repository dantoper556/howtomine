from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from .forms import *
from django.forms import formset_factory

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
    data["cnt"] = 1
    # data["forms"] = [ChooseCardForm()]
    data["forms"] = formset_factory(ChooseCardForm, extra=data["cnt"])
    # if (request.method == "POST"):
    #     t1 = request.POST['form-0-cards']
    #     print(t1)
    if (request.method == "POST"):
        if ("inc" in request.POST):
            print(request.POST)
            data["cnt"] = int(request.POST['form-0-cnt']) + 1
            data["forms"].extra = data["cnt"]
            # t1 = ChooseCardForm(request.POST)
            # if (t1.is_valid()):
            #     if (t1.cleaned_data["cnt"] != None):
            #         data["cnt"] = t1.cleaned_data["cnt"] + 1
            #         data["forms"] = [ChooseCardForm() for i in range(data["cnt"])]
            #         return render(request, 'calc_profit_page.html', context=data)
            #     # return HttpResponse(t1.cleaned_data["cnt"])
            # return HttpResponse("not ok")
        elif (sum([el.count("del") for el in request.POST.keys()]) > 0):
            print([el for el in request.POST.keys()])
            if (int(request.POST['form-0-cnt']) > 1):
                data["cnt"] = int(request.POST['form-0-cnt']) - 1
                print(data["cnt"])
                data["forms"].extra = data["cnt"]
                return render(request, 'calc_profit_page.html', context=data)
        else:
            return HttpResponse("not ok")
        # return render(request, 'calc_profit_page.html', context={"cards": ['testik']})
    return render(request, 'calc_profit_page.html', context=data)
