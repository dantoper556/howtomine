from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from .forms import *
from .presenters import *
from django.forms import formset_factory
import requests
from bs4 import BeautifulSoup as bs
from .calculators import calc_config_profit, calc_asics_config_profit, calc_duals_config_profit, make_offer

def main_page(request):
    return render(request, 'main_page.html')

def make_conf_page(request):
    return render(request, 'make_conf_page.html')

def calc_profit_page(request):
    class VCParser:
        def __init__(self, ind: int, quantity: int = 1) -> None:
            self.ind = ind
            self.quantity = quantity
        
        def __repr__(self) -> str:
            return f'|{self.ind}: {self.quantity}|'
        
        def get_query(self, req, qtype: str) -> str:
            return req[f'form-{self.ind}-{qtype}']

    data = dict()
    data["cards"] = []
    for obj in VideoCard.objects.all():
        data["cards"].append(obj.name)

    data["cnt"] = 1
    data["forms"] = formset_factory(ChooseCardForm, extra=data["cnt"])
    data["form_vals"] = [0]
    data["form_quant"] = [1]
    data["picked_cards"] = []
    data["elec"] = 0.1
    data["profit"] = []
    
    if (request.method == "POST"):
        data["cnt"] = int(request.POST['form-0-cnt'])
        data["elec"] = float(request.POST['electricity'])
        sz = data["cnt"]
        vcl = []
        for i in range(sz): vcl.append(VCParser(i))

        flag = 0
        if ("inc" in request.POST):
            data["cnt"] += 1
            flag = 1
        elif (sum([el.count("del") for el in request.POST.keys()]) > 0):
            if (int(request.POST['form-0-cnt']) > 1):
                data["cnt"] -= 1

                for el in request.POST.keys():
                    if (el.count('del') > 0):
                        s = el.split(' ')
                        vcl.pop(int(s[1]) - 1)
            flag = 2
        elif ("sbm" in request.POST):
            config = dict()
            for el in VideoCard.objects.all(): config[el] = 0
            for el in vcl: 
                config[VideoCard.objects.all()[int(el.get_query(request.POST, "cards"))]] += int(el.get_query(request.POST, "quantity"))

            raw_profit = calc_config_profit(config, data["elec"])
            raw_duals_profit = calc_duals_config_profit(raw_profit, config, data["elec"])
            raw_offer = make_offer(config)
            print(raw_offer)
            data["prices"] = raw_offer
            data["profit"] = make_table_vc(data, raw_profit)
            data["duals"] = make_duals_table(raw_duals_profit, data)
        
        data["forms"].extra = data["cnt"]
        tl, tq = [], []
        for el in vcl: 
            tl.append(el.get_query(request.POST, "cards"))
            tq.append(el.get_query(request.POST, "quantity"))
        data["form_vals"] = tl
        data["form_quant"] = tq

    return render(request, 'calc_profit_page.html', context=data)

def calc_asics_profit_page(request):
    class VCParser:
        def __init__(self, ind: int, quantity: int = 1) -> None:
            self.ind = ind
            self.quantity = quantity
        
        def __repr__(self) -> str:
            return f'|{self.ind}: {self.quantity}|'
        
        def get_query(self, req, qtype: str) -> str:
            return req[f'form-{self.ind}-{qtype}']
    
    data = dict()
    data["cards"] = []
    for obj in Asics.objects.all():
        data["cards"].append(obj.name)

    data["cnt"] = 1
    data["forms"] = formset_factory(ChooseAsicsForm, extra=data["cnt"])
    data["form_vals"] = [0]
    data["form_quant"] = [1]
    data["picked_cards"] = []
    data["elec"] = 0.1

    data["profit"] = dict()

    if (request.method == "POST"):
        data["cnt"] = int(request.POST['form-0-cnt'])
        data["elec"] = float(request.POST['electricity'])
        sz = data["cnt"]
        vcl = []
        for i in range(sz): vcl.append(VCParser(i))

        if ("inc" in request.POST):
            data["cnt"] += 1
        elif (sum([el.count("del") for el in request.POST.keys()]) > 0):
            if (int(request.POST['form-0-cnt']) > 1):
                data["cnt"] -= 1

                for el in request.POST.keys():
                    if (el.count('del') > 0):
                        s = el.split(' ')
                        vcl.pop(int(s[1]) - 1)
        elif ("sbm" in request.POST):
            # print(request.POST)

            config = dict()
            for el in Asics.objects.all(): config[el] = 0
            for el in vcl:
                config[Asics.objects.all()[int(el.get_query(request.POST, "cards"))]] += int(el.get_query(request.POST, "quantity"))
            
            # for key, val in config.items():
            #     print(key.hashrate_no_code, val)

            raw_profit = calc_asics_config_profit(config, data["elec"])
            data["raw"] = raw_profit
            data["profit"] = make_table_asics(data, raw_profit)
        
        data["forms"].extra = data["cnt"]
        tl, tq = [], []
        for el in vcl: 
            tl.append(el.get_query(request.POST, "cards"))
            tq.append(el.get_query(request.POST, "quantity"))
        data["form_vals"] = tl
        data["form_quant"] = tq
    
    return render(request, 'calc_asics_profit_page.html', context=data)