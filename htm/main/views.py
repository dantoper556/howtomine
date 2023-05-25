from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from .forms import *
from django.forms import formset_factory
import requests
from bs4 import BeautifulSoup as bs

def main_page(request):
    return render(request, 'main_page.html')

def make_conf_page(request):
    return render(request, 'make_conf_page.html')

def calc_config_profit(config: dict(), elec_price: float) -> dict():
    profit = dict()
    for obj in CryptoCoin.objects.all(): profit[obj] = [0, 0, 0, 0, 0]
    for key, quantity in config.items():
        for obj in CryptoCoin.objects.all():
            url = f"https://www.hashrate.no/gpus/{key.hashrate_no_code}/{obj.hashrate_no_code}"
            req = requests.get(url)
            raw_text = bs(req.text, features="html.parser")
            raw_desc = raw_text.find_all("span", {"class", "description"})
            desc = str(bs(str(raw_desc), features="html.parser").text)

            if ("Mh/s" not in desc):
                pass
            else:
                w = 0
                parsed_table = raw_text.find_all("td")
                for el in parsed_table:
                    if ("watt" in str(el)):
                        w = int(el.text.split()[0]) + 20
                        break

                mt = desc.split(" Mh/s ")
                profit[obj][0] += float(mt[0].split(" ")[-1]) * quantity

                url = f"https://www.hashrate.no/coins/{obj.hashrate_no_code.lower()}"
                req = requests.get(url)
                raw_text = bs(req.text, features="html.parser")
                profit_1mhs = raw_text.find_all("td", {"class", "infoFocus"})[1]
                
                profit[obj][1] = profit[obj][0] * float(profit_1mhs.text.split(" ")[0])
                usd_per_coin = float(raw_text.find_all("font", {"class", "infoFocus"})[0].text[1:])

                profit[obj][2] = profit[obj][1] * usd_per_coin
                profit[obj][3] += quantity * w * 24 / 1000
                profit[obj][4] += (quantity * w * 24 / 1000 * elec_price) / usd_per_coin


    return profit

def calc_profit_page(request):
    class VCParser:
        def __init__(self, ind: int, quantity: int = 1) -> None:
            self.ind = ind
            self.quantity = quantity
        
        def __repr__(self) -> str:
            return f'|{self.ind}: {self.quantity}|'
        
        def get_query(self, req, qtype: str) -> str:
            return req[f'form-{self.ind}-{qtype}']

    b = 0
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

    data["profit"] = dict()
    for el in CryptoCoin.objects.all(): data["profit"][el.name] = [0, 0]
    
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
            # print(config)
            raw_profit = calc_config_profit(config, data["elec"])
            # print(raw_profit)
            profit = dict()
            for obj in CryptoCoin.objects.all():
                profit[obj.name] = [
                    'hashrate',                     #0
                    'd_in_coin',                    #1
                    'm_in_coin',                    #2
                    'd_in_fiat',                    #3
                    'm_in_fiat',                    #4
                    'pwr_cons',                     #5
                    'pwr_cons_usd',                 #6
                    'd_profit',                     #7
                    'm_profit',                     #8
                ]
            
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
            
            # print(profit)
            data["profit"] = profit
        
        data["forms"].extra = data["cnt"]
        tl, tq = [], []
        for el in vcl: 
            tl.append(el.get_query(request.POST, "cards"))
            tq.append(el.get_query(request.POST, "quantity"))
        data["form_vals"] = tl
        data["form_quant"] = tq

    return render(request, 'calc_profit_page.html', context=data)
