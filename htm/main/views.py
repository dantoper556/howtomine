from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from .forms import *
from .presenters import *
from django.forms import formset_factory
import requests
from bs4 import BeautifulSoup as bs
from .calculators import calc_config_profit, calc_asics_config_profit, calc_duals_config_profit, make_offer
import json
from math import *


def main_page(request):
    return render(request, 'main_page.html')


def make_conf_page(request):
    data = {}
    data["elec"] = 0.1
    data["budget"] = 1000.0
    data["cnt"] = 0

    # список всех карт
    config = {}
    for el in VideoCard.objects.all():
        config[el] = 1
    cards, exist = make_offer(config)
    # получение данных от пользователя
    if (request.method == "POST"):
        try:
            data["elec"] = float(request.POST["electricity"])
        except ValueError:
            data["elec"] = 0
        try:
            data["budget"] = float(request.POST["budget"])
        except ValueError:
            data["budget"] = 0
        try:
            data["cnt"] = int(request.POST["cnt"])
        except ValueError:
            data["cnt"] = 0

    # состовляем список из карт со значением отношения доходности к цене
    vals = dict()
    srt_l = []
    for el in cards.keys():
        t = dict()
        t[el] = 1
        w = float(make_table_vc(data, calc_config_profit(t, data["elec"]))[0]["clear_prf_usd"].split()[0])
        # print(":", el, w)
        vals[el] = [w, cards[el][0]]
        srt_l.append([w / cards[el][0], el])

    cnt = data["cnt"]
    if (cnt == 0):
        cnt = 1e9

    # првоеряем, есть ли хотя бы одна доходная конфигурация
    data["cards"] = cards
    srt_l.sort(reverse=True)
    print(srt_l)
    data["status"] = 0
    if (srt_l[0][0] < 0): data["status"] = 1
    res = dict()
    for el in VideoCard.objects.all():
        res[el] = 0
    # сначала набираем много самых выгодных карт
    res[srt_l[0][1]] = min(cnt, data["budget"] // vals[srt_l[0][1]][1])
    rcnt = res[srt_l[0][1]]
    left = data["budget"] - rcnt * vals[srt_l[0][1]][1]
    while (1):
        ok = 0
        for el in res.keys():
            for nw in cards.keys():
                if (res[el] > 0):
                    if (left + cards[el][0] - cards[nw][0] > 0):
                        if (vals[nw] > vals[el]):
                            res[el] -= 1
                            res[nw] += 1
                            ok = 1
                            left += cards[el][0] - cards[nw][0]
                            # если можем улучшить ответ заменой какой-то карты на другую - улучшаем
        if (ok == 0):
            break
    
    clc_f = calc_config_profit(res, data["elec"])
    clc_f_d = calc_duals_config_profit(clc_f, res, data["elec"])
    raw_offer, exist = make_offer(res)
    data["profit"] = make_table_vc(data, clc_f)
    data["duals"] = make_duals_table(clc_f_d, data)
    data["total_price"] = 0
    data["payback"] = 0
    data["exists"] = exist
    data["prices"] = raw_offer
    # print(exist)
    # окупаемость и общая цена
    if (exist):
        for card in res.keys():
            if (res[card] > 0):
                data["total_price"] += round(res[card] * raw_offer[card][0], 2)
        mx = 0
        for l in data["profit"]:
            mx = max(mx, float(l["clear_prf_usd"].split()[0]))
        for l in data["duals"]:
            mx = max(mx, float(l["clear_prf_usd"]))
        # print(mx)
        if (mx == 0):
            data["payback"] = -1
        else:
            data["payback"] = round(data["total_price"] / mx + 1)

    data["total_price"] = round(data["total_price"], 2)
    # отправляем таблицу на html страницу
    resl = []
    for el in res.keys():
        if (res[el] > 0):
            resl.append([str(el), int(res[el])])
    data["res"] = resl
    return render(request, 'make_conf_page.html', context=data)


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
        # считывем форму
        data["cnt"] = int(request.POST['form-0-cnt'])
        try:
            data["elec"] = float(request.POST['electricity'])
        except ValueError:
            data["elec"] = 0
        sz = data["cnt"]
        vcl = []
        for i in range(sz): vcl.append(VCParser(i))

        flag = 0
        if ("inc" in request.POST):
            # добавление поля к форме
            data["cnt"] += 1
            flag = 1
        elif (sum([el.count("del") for el in request.POST.keys()]) > 0):
            # удаление поля из формы
            if (int(request.POST['form-0-cnt']) > 1):
                data["cnt"] -= 1

                for el in request.POST.keys():
                    if (el.count('del') > 0):
                        s = el.split(' ')
                        vcl.pop(int(s[1]) - 1)
            flag = 2
        elif ("sbm" in request.POST):
            # подсчет прибыли
            # считываем конфигурацию
            config = dict()
            for el in VideoCard.objects.all(): config[el] = 0
            for el in vcl: 
                try:
                    config[VideoCard.objects.all()[int(el.get_query(request.POST, "cards"))]] += ceil(float(el.get_query(request.POST, "quantity")))
                except ValueError:
                    config[VideoCard.objects.all()[int(el.get_query(request.POST, "cards"))]] += 1

            # считаем профит
            raw_profit = calc_config_profit(config, data["elec"])
            raw_duals_profit = calc_duals_config_profit(raw_profit, config, data["elec"])
            raw_offer, exist = make_offer(config)
            # заполняем мапу для вывода
            data["exists"] = exist
            data["prices"] = raw_offer
            data["profit"] = make_table_vc(data, raw_profit)
            data["duals"] = make_duals_table(raw_duals_profit, data)
            data["total_price"] = 0
            data["payback"] = 0
            # общая цена и окупаемость
            if (exist):
                for card in config.keys():
                    if (config[card] > 0):
                        data["total_price"] += config[card] * raw_offer[card][0]
                mx = 0
                for l in data["profit"]:
                    mx = max(mx, float(l["clear_prf_usd"].split()[0]))
                for l in data["duals"]:
                    mx = max(mx, float(l["clear_prf_usd"]))
                print(mx)
                if (mx == 0):
                    data["payback"] = -1
                else:
                    data["payback"] = round(data["total_price"] / mx)
        data["total_price"] = round(data["total_price"], 2)

        # генерируем формы 
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
        # считываем форму
        data["cnt"] = int(request.POST['form-0-cnt'])
        try:
            data["elec"] = float(request.POST['electricity'])
        except ValueError:
            data["elec"] = 0
        sz = data["cnt"]
        vcl = []
        for i in range(sz): vcl.append(VCParser(i))

        if ("inc" in request.POST):
            # добавление поля
            data["cnt"] += 1
        elif (sum([el.count("del") for el in request.POST.keys()]) > 0):
            # удаление поля
            if (int(request.POST['form-0-cnt']) > 1):
                data["cnt"] -= 1

                for el in request.POST.keys():
                    if (el.count('del') > 0):
                        s = el.split(' ')
                        vcl.pop(int(s[1]) - 1)
        elif ("sbm" in request.POST):
            # подсчет прибыли
            config = dict()
            for el in Asics.objects.all(): config[el] = 0
            for el in vcl:
                try:
                    config[Asics.objects.all()[int(el.get_query(request.POST, "cards"))]] += ceil(float(el.get_query(request.POST, "quantity")))
                except ValueError:
                    config[Asics.objects.all()[int(el.get_query(request.POST, "cards"))]] += 1

            # заполняем мапу для вывода
            raw_profit = calc_asics_config_profit(config, data["elec"])
            data["raw"] = raw_profit
            data["profit"] = make_table_asics(data, raw_profit)
        
        # генерируем формы
        data["forms"].extra = data["cnt"]
        tl, tq = [], []
        for el in vcl: 
            tl.append(el.get_query(request.POST, "cards"))
            tq.append(el.get_query(request.POST, "quantity"))
        data["form_vals"] = tl
        data["form_quant"] = tq
    
    return render(request, 'calc_asics_profit_page.html', context=data)


def present_cards(request):
    data = dict()
    f3 = open("./main/jsons/vcards.json", 'r')
    data["vcards_list"] = dict(json.load(f3))
    data["vcards_list"].pop("time")
    data["vcards_list"].pop("usd_rub")
    data["res"] = []
    data["sort_pars"] = ""
    if (request.method == "POST"):
        try:
            ql = float(request.POST["minv"])
        except ValueError:
            ql = 0
        try:
            qr = float(request.POST["maxv"])
        except ValueError:
            qr = 1000000000
        
        # print(ql, qr)
        # фильтр по цене
        for k in data["vcards_list"].keys():
            if (data["vcards_list"][k][0] != '-' and ql <= data["vcards_list"][k][0] <= qr):
                data["res"].append([k, data["vcards_list"][k]])
        data["res"].sort(key=lambda a: a[1][0])
        # сортировки
        if ("sort" in request.POST.keys()):
            if (request.POST["sort"] == "sort1"):
                data["res"].sort(key=lambda a: a[1][0])
                data["sort_pars"] += "Сортровать по возрастанию цены, "
            elif (request.POST["sort"] == "sort2"):
                data["res"].sort(key=lambda a: a[1][0], reverse=True)
                data["sort_pars"] += "Сортровать по убыванию цены, "
        data["sort_pars"] += f"от {ql} $ до {qr} $"
        print(request.POST)
    else:
        # при первом открытии страницы добавляем все
        for k in data["vcards_list"].keys():
            data["res"].append([k, data["vcards_list"][k]])
    return render(request, 'present_all.html', context=data)
