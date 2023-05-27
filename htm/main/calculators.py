from .models import *
from .forms import *
import requests
from bs4 import BeautifulSoup as bs

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
                        w = int(el.text.split()[0])
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

def calc_asics_config_profit(config: dict(), elec_price: float):
    profit = dict()
    for asics, quantity in config.items():  
        if (quantity == 0): continue
        profit[asics] = dict()

    #     print(asics, quantity)
        url = f"https://hashrate.no/asics/{asics.hashrate_no_code}"
        req = requests.get(url)
        raw_text = bs(req.text, features="html.parser")
        raw_coinname = raw_text.find_all("span", {"class", "deviceHeader"})
        
        coins = []
        for el in raw_coinname:
            coinname = el.text
            for coin in CryptoCoin.objects.all():
                if (coinname == coin.name):
                    print("found", coin.name)
                    profit[asics][coin] = [0, 0, 0, 0, 0]
                    coins.append(coin)

        mhs = []
        parsed_table = raw_text.find_all("td")
        for el in parsed_table:
            if ("h/s" in str(el.text)):
                hs = float(el.text.split()[0])
                # if (el.text.split()[1][0] == "T"): hs *= 1000000
                mhs.append(hs)
        print(mhs)

        watts = []
        parsed_table = raw_text.find_all("td")
        for el in parsed_table:
            if (" w" in str(el.text)):
                # print(float(el.text.split()[0]))
                watts.append(float(el.text.split()[0]))
        print(watts)
        
        
        
        for i in range(len(coins)):
            obj = coins[i]
            profit[asics][coins[i]][0] += mhs[i] * quantity

            url = f"https://www.hashrate.no/coins/{obj.hashrate_no_code.lower()}"
            req = requests.get(url)
            raw_text = bs(req.text, features="html.parser")
            profit_1mhs = raw_text.find_all("td", {"class", "infoFocus"})[1]
            
            profit[asics][obj][1] = profit[asics][obj][0] * float(profit_1mhs.text.split(" ")[0])
            usd_per_coin = float(raw_text.find_all("font", {"class", "infoFocus"})[0].text[1:])

            profit[asics][obj][2] = profit[asics][obj][1] * usd_per_coin
            profit[asics][obj][3] += quantity * watts[i] * 24 / 1000
            # profit[obj][3] += quantity * watts[i] * 24 / 1000
            profit[asics][obj][4] += (quantity * watts[i] * 24 / 1000 * elec_price) / usd_per_coin
            
    #     # for i in range(len(raw_coinname)):
    return profit