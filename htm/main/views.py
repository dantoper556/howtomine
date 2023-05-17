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
    data["form_vals"] = [0]
    # if (request.method == "POST"):
    #     t1 = request.POST['form-0-cards']
    #     print(t1)
    if (request.method == "POST"):
        data["cnt"] = int(request.POST['form-0-cnt'])
        tl = []
        sz = data["cnt"]
        for i in range(sz):
            tl.append(request.POST['form-'+str(i)+'-cards'])
        # print(tl)
        data["form_vals"] = tl

        if ("inc" in request.POST):
            # print(request.POST)
            data["cnt"] += 1
            data["forms"].extra = data["cnt"]
        elif (sum([el.count("del") for el in request.POST.keys()]) > 0):
            # print([el for el in request.POST.keys()])
            if (int(request.POST['form-0-cnt']) > 1):
                data["cnt"] -= 1
                # print(data["cnt"])
                data["forms"].extra = data["cnt"]

                for el in request.POST.keys():
                    if (el.count('del') > 0):
                        s = el.split(' ')
                        # print(int(s[1]) - 1)
                        data["form_vals"].pop(int(s[1]) - 1)
        
        # return render(request, 'calc_profit_page.html', context=data)
        # return render(request, 'calc_profit_page.html', context={"cards": ['testik']})
    return render(request, 'calc_profit_page.html', context=data)
