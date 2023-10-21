from .models import *
from .forms import *
import requests
import json
import time
from bs4 import BeautifulSoup as bs

def update_jsons():
    sleep = 3600

    f1 = open("./main/jsons/coins.json")
    dat = json.load(f1)
    last_upd = dat["time"]

    for coin in CryptoCoin.objects.all():
        if (time.time() - last_upd > sleep or coin.name not in dat["parsed"].keys()):
            dat["parsed"][coin.name] = {}
            url = f"https://www.hashrate.no/coins/{coin.hashrate_no_code.lower()}"
            req = requests.get(url)
            raw_text = bs(req.text, features="html.parser")
            profit_1mhs = raw_text.find_all("td", {"class", "infoFocus"})[1]
            usd_per_coin = float(raw_text.find_all("font", {"class", "infoFocus"})[0].text[1:])
            dat["parsed"][coin.name]["profit_1mhs"] = float(profit_1mhs.text.split(" ")[0])
            dat["parsed"][coin.name]["usd_per_coin"] = float(raw_text.find_all("font", {"class", "infoFocus"})[0].text[1:])
            dat["time"] = time.time()
    
    json.dump(dat, open("./main/jsons/coins.json", 'w'))

    f2 = open("./main/jsons/cards.json")
    dat = json.load(f2)
    last_upd = dat["time"]

    for card in VideoCard.objects.all():
        if (card.name not in dat["parsed"].keys()): dat["parsed"][card.name] = {}
        for coin in CryptoCoin.objects.all():
            if (time.time() - last_upd > sleep or coin.name not in dat["parsed"][card.name].keys()):
                dat["parsed"][card.name][coin.name] = {}
                url = f"https://www.hashrate.no/gpus/{card.hashrate_no_code}/{coin.hashrate_no_code}"
                req = requests.get(url)
                raw_text = bs(req.text, features="html.parser")
                raw_desc = raw_text.find_all("span", {"class", "description"})
                desc = str(bs(str(raw_desc), features="html.parser").text)

                w = 0
                parsed_table = raw_text.find_all("td")
                for el in parsed_table:
                    if ("watt" in str(el)):
                        w = int(el.text.split()[0])
                        break

                mt = desc.split(" Mh/s ")
                dat["parsed"][card.name][coin.name]["pwr"] = w
                try:
                    dat["parsed"][card.name][coin.name]["hsh"] = float(mt[0].split(" ")[-1])
                except Exception:
                    dat["parsed"][card.name][coin.name]["hsh"] = 0
                
                dat["time"] = time.time()

    json.dump(dat, open("./main/jsons/cards.json", 'w'))

    f3 = open("./main/jsons/vcards.json", 'r')
    usd_rub = 100
    res = {}
    dat = dict(json.load(f3))
    res = dat
    last_upd = dat["time"]
    if (time.time() - last_upd > sleep):
        pr_g = requests.get("https://exchange-rates.abstractapi.com/v1/live/?api_key=6f5477586faa4c1f9a33ecf8f1aa5f64&base=USD&target=RUB")
        # print(pr_g)
        usd_rub = pr_g.json()['exchange_rates']['RUB']
        res["usd_rub"] = usd_rub
    # print(list(dat.keys()))
    # print(time.time() - last_upd > 3600)
    for el in VideoCard.objects.all():
        if (time.time() - last_upd > sleep or str(el) not in dat.keys()):
            url = "https://n-katalog.ru/search?keyword=" + el.name.replace(' ', '+')
            req = requests.get(url)
            raw_text = bs(req.text, features="html.parser")
            price_list = raw_text.find_all("div", {"class", "model-price-range"})
            l = []
            for it in price_list:
                a = it.find_all('a', href=True)[0]
                price = int(a.text.split()[0])
                link = "https://n-katalog.ru" + a['href']
                if (price > 0): l.append((round(price / res["usd_rub"], 2), link))
                # print(int(a.text.split()[0]), a['href'])
                # print(a)
            l.sort()
            if (len(l) > 0): res[str(el)] = l[0]
            else: res[str(el)] = "-"
            res["time"] = time.time()
            print(el)
    json.dump(res, open("./main/jsons/vcards.json", 'w'))


def calc_config_profit(config: dict(), elec_price: float) -> dict():
    update_jsons()

    f1 = open("./main/jsons/coins.json")
    coins_inf = json.load(f1)
    # print(dat)

    f2 = open("./main/jsons/cards.json")
    cards_inf = json.load(f2)

    profit = dict()
    for obj in CryptoCoin.objects.all(): profit[obj] = [0, 0, 0, 0, 0]
    for key, quantity in config.items():
        for coin in CryptoCoin.objects.all():
            # print(key.name, coin.name, cards_inf["parsed"][key.name][coin.name], coins_inf["parsed"][coin.name])
            # print(key, quantity)
            profit[coin][0] += cards_inf["parsed"][key.name][coin.name]["hsh"] * quantity

            profit_1mhs = coins_inf["parsed"][coin.name]["profit_1mhs"]
            usd_per_coin = coins_inf["parsed"][coin.name]["usd_per_coin"]
            w = cards_inf["parsed"][key.name][coin.name]["pwr"]

            # print(profit_1mhs, usd_per_coin, w)
            
            profit[coin][1] = profit[coin][0] * profit_1mhs
            profit[coin][2] = profit[coin][1] * usd_per_coin
            profit[coin][3] += quantity * w * 24 / 1000
            profit[coin][4] += (quantity * w * 24 / 1000 * elec_price) / usd_per_coin

    return profit

def calc_duals_config_profit(solos: dict(), config: dict(), elec_price: float) -> dict():
    f2 = open("./main/jsons/cards.json")
    cards_inf = json.load(f2)

    profit = dict()
    for pair in Duals.objects.all():
        first, second = pair.pair.all()
        if (solos[first][0] > solos[second][0]):
            t = first
            first = second
            second = t

        profit[pair] = [
            [solos[first][0], solos[second][0] / 2],
            solos[first][2] + solos[second][2] / 2,
            (solos[second][0] / 2) / max(0.0001, solos[first][0]),
            [first, second],
            (solos[first][3] + solos[second][3]) / 2,
        ]    

    return profit

def calc_asics_config_profit(config: dict(), elec_price: float) -> dict():
    update_jsons()

    f1 = open("./main/jsons/coins.json")
    coins_inf = json.load(f1)

    profit = dict()
    for asics, quantity in config.items():  
        if (quantity == 0): continue
        profit[asics] = dict()

        url = f"https://hashrate.no/asics/{asics.hashrate_no_code}"
        req = requests.get(url)
        raw_text = bs(req.text, features="html.parser")
        raw_coinname = raw_text.find_all("span", {"class", "deviceHeader"})
        
        coins = []
        for el in raw_coinname:
            coinname = el.text
            for coin in CryptoCoin.objects.all():
                if (coinname == coin.name):
                    # print("found", coin.name)
                    profit[asics][coin] = [0, 0, 0, 0, 0]
                    coins.append(coin)

        mhs = []
        parsed_table = raw_text.find_all("td")
        for el in parsed_table:
            if ("h/s" in str(el.text)):
                hs = float(el.text.split()[0])
                mhs.append(hs)

        watts = []
        parsed_table = raw_text.find_all("td")
        for el in parsed_table:
            if (" w" in str(el.text)):
                watts.append(float(el.text.split()[0]))
                
        for i in range(len(coins)):
            coin = coins[i]
            profit[asics][coin][0] += mhs[i] * quantity

            profit_1mhs = coins_inf["parsed"][coin.name]["profit_1mhs"]
            usd_per_coin = coins_inf["parsed"][coin.name]["usd_per_coin"]
            
            profit[asics][coin][1] = profit[asics][coin][0] * profit_1mhs

            profit[asics][coin][2] = profit[asics][coin][1] * usd_per_coin
            profit[asics][coin][3] += quantity * watts[i] * 24 / 1000
            profit[asics][coin][4] += (quantity * watts[i] * 24 / 1000 * elec_price) / usd_per_coin
            
    return profit


def make_offer(config) -> dict():
    update_jsons()

    res = dict()
    status = 1
    f = open("./main/jsons/vcards.json", 'r')
    dat = dict(json.load(f))
    for el in config.keys():
        if (config[el] > 0):
            # print(el)
            l = dat[str(el)]
            if (l == '-'): status = 0
            else: res[el] = l
    return (res, status)
