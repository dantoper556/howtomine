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

def calc_profit_page(request):
    class VCParser:
        def __init__(self, ind: int, quantity: int = 1) -> None:
            self.ind = ind
            self.quantity = quantity
        
        def __repr__(self) -> str:
            return f'|{self.ind}: {self.quantity}|'
        
        def get_query(self, req, qtype: str) -> str:
            return req[f'form-{self.ind}-{qtype}']
        
        def test_parse(self, req) -> str:
            ind = int(self.get_query(req, "cards"))
            quantity = self.get_query(req, "quantity")
            url = "https://www.hashrate.no/gpus/" + str(VideoCard.objects.all()[ind].hashrate_no_code)
            # print(url)
            r = requests.get(url)
            txt = bs(r.text)
            d1 = txt.find_all("div", {"class", "description"})[0]
            t1 = bs(str(d1)).text
            return t1
            # print(t1)

    b = 0
    data = dict()
    data["cards"] = []
    for obj in VideoCard.objects.all():
        data["cards"].append(obj.name)

    data["cnt"] = 1
    data["forms"] = formset_factory(ChooseCardForm, extra=data["cnt"])
    data["form_vals"] = [0]
    data["form_quant"] = [1]
    data["picked_cards"] = dict()
    
    if (request.method == "POST"):
        data["cnt"] = int(request.POST['form-0-cnt'])
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
            d = dict()
            for el in vcl: 
                d[VideoCard.objects.all()[int(el.get_query(request.POST, "cards"))]] = el.test_parse(request.POST)
            # for el in vcl:
                # d[VideoCard.objects.all()[int(el.get_query(request.POST, "cards"))].name] += int(el.get_query(request.POST, "quantity"))
            
            data["picked_cards"] = d

            for key in data["picked_cards"].keys():
                for obj in CryptoCoin.objects.all():
                    url =f"https://www.hashrate.no/gpus/{key.hashrate_no_code}/{obj.hashrate_no_code}"
                    r = requests.get(url)
                    txt = bs(r.text)
                    d1 = txt.find_all("span", {"class", "description"})
                    t1 = str(bs(str(d1)).text)
                    print(url)
                    if ("Mh/s" not in t1):
                        pass
                    else:
                        mt = t1.split(" Mh/s ")
                        print(float(mt[0].split(" ")[-1]), "Mh/s")
        
        data["forms"].extra = data["cnt"]
        tl, tq = [], []
        for el in vcl: 
            tl.append(el.get_query(request.POST, "cards"))
            tq.append(el.get_query(request.POST, "quantity"))
        data["form_vals"] = tl
        data["form_quant"] = tq

    return render(request, 'calc_profit_page.html', context=data)
