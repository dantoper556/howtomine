from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from .forms import *
from django.forms import formset_factory
import requests
from bs4 import BeautifulSoup as bs
from .calculators import calc_config_profit, calc_asics_config_profit

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
    # for el in CryptoCoin.objects.all(): data["profit"][el.name] = [0, 0]
    
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
            print(request.POST)

            config = dict()
            for el in VideoCard.objects.all(): config[el] = 0
            for el in vcl: 
                config[VideoCard.objects.all()[int(el.get_query(request.POST, "cards"))]] += int(el.get_query(request.POST, "quantity"))

            raw_profit = calc_config_profit(config, data["elec"])
            # for obj in CryptoCoin.objects.all():
            #     profit[obj.name] = [
            #         'hashrate',                     #0
            #         'd_in_coin',                    #1
            #         'm_in_coin',                    #2
            #         'd_in_fiat',                    #3
            #         'm_in_fiat',                    #4
            #         'pwr_cons',                     #5
            #         'pwr_cons_usd',                 #6
            #         'd_profit',                     #7
            #         'm_profit',                     #8
            #     ]
            
            profit = []
            for key, val in raw_profit.items():
                if (val[0] == 0): continue
                profit.append([
                    key.name,
                    f'{(round(val[0], 2))} Mh/s',                                               #0
                    f'{(round(val[1], 2))} {key.hashrate_no_code}',                             #1
                    f'{(round(val[1] * 30, 2))} {key.hashrate_no_code}',                        #2
                    f'{(round(val[2], 2))} $',                                                  #3
                    f'{(round(val[2] * 30, 2))} $',                                             #4
                    f'{(round(val[3], 2))} kWh',                                                #5
                    f'{(round(val[3] * data["elec"], 2))} $',                                   #6
                    f'{(round(val[3] * 30, 2))} kWh',                                           #7
                    f'{(round(val[3] * 30 * data["elec"], 2))} $',                              #8
                    f'{(round(val[2] - val[3] * data["elec"], 2))} $',                          #9
                    f'{(round(val[2] * 30 - val[3] * data["elec"] * 30, 2))} $',                #10
                    f'{(round(val[1] - val[4], 2))} {key.hashrate_no_code}',                    #11
                    f'{(round(val[1] * 30 - val[4] * 30, 2))} {key.hashrate_no_code}',          #12
                ])
            profit.sort(key=lambda a: float(a[10].split()[0]), reverse=True)
            print(profit)
            data["profit"] = profit
        
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
    # for el in CryptoCoin.objects.all(): data["profit"][el.name] = [0, 0]

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
            print(request.POST)

            config = dict()
            for el in Asics.objects.all(): config[el] = 0
            for el in vcl:
                config[Asics.objects.all()[int(el.get_query(request.POST, "cards"))]] += int(el.get_query(request.POST, "quantity"))
            
            for key, val in config.items():
                print(key.hashrate_no_code, val)

            raw_profit = calc_asics_config_profit(config, data["elec"])
            profit = dict()            
            for key, val in raw_profit.items():
                profit[key.name] = [
                    f'{(round(val[0], 2))} Mh/s',                                               #0
                    f'{(round(val[1], 2))} {key.hashrate_no_code}',                             #1
                    f'{(round(val[1] * 30, 2))} {key.hashrate_no_code}',                        #2
                    f'{(round(val[2], 2))} $',                                                  #3
                    f'{(round(val[2] * 30, 2))} $',                                             #4
                    f'{(round(val[3], 2))} kWh',                                                #5
                    f'{(round(val[3] * data["elec"], 2))} $',                                   #6
                    f'{(round(val[3] * 30, 2))} kWh',                                           #7
                    f'{(round(val[3] * 30 * data["elec"], 2))} $',                              #8
                    f'{(round(val[2] - val[3] * data["elec"], 2))} $',                          #9
                    f'{(round(val[2] * 30 - val[3] * data["elec"] * 30, 2))} $',                #10
                    f'{(round(val[1] - val[4], 2))} {key.hashrate_no_code}',                    #11
                    f'{(round(val[1] * 30 - val[4] * 30, 2))} {key.hashrate_no_code}',          #12
                ]

            data["profit"] = profit
        
        data["forms"].extra = data["cnt"]
        tl, tq = [], []
        for el in vcl: 
            tl.append(el.get_query(request.POST, "cards"))
            tq.append(el.get_query(request.POST, "quantity"))
        data["form_vals"] = tl
        data["form_quant"] = tq
    
    return render(request, 'calc_asics_profit_page.html', context=data)