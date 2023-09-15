def make_table_vc(data: dict, raw_profit: dict) -> dict:
    profit = []
    for coin, val in raw_profit.items():
        if (val[0] == 0): continue
        profit.append({
            "coin": coin.name,
            "hsh": f'{(round(val[0], 2))} Mh/s',
            "prf_coin": f'{(round(val[1], 2))} {coin.hashrate_no_code}',
            "mnh_prf_coin": f'{(round(val[1] * 30, 2))} {coin.hashrate_no_code}',
            "prf_usd": f'{(round(val[2], 2))} $',
            "mnh_prf_usd": f'{(round(val[2] * 30, 2))} $',
            "pwr_cons": f'{(round(val[3], 2))} kWh',
            "pwr_cons_usd": f'{(round(val[3] * data["elec"], 2))} $',
            "mnh_pwr_cons": f'{(round(val[3] * 30, 2))} kWh',
            "mnh_pwr_cons_usd": f'{(round(val[3] * 30 * data["elec"], 2))} $',
            "clear_prf_usd": f'{(round(val[2] - val[3] * data["elec"], 2))} $',
            "mnh_clear_prf_usd": f'{(round(val[2] * 30 - val[3] * data["elec"] * 30, 2))} $',
            "clear_prf_coin": f'{(round(val[1] - val[4], 2))} {coin.hashrate_no_code}',
            "mnh_clear_prf_coin": f'{(round(val[1] * 30 - val[4] * 30, 2))} {coin.hashrate_no_code}',
        })
    profit.sort(key=lambda a: float(a["clear_prf_coin"].split()[0]), reverse=True)

    return profit

def make_duals_table(raw_duals_profit, data):
    duals = []
    for key, val in raw_duals_profit.items():
        duals.append({
            "name": val[3],
            "par": str(key),
            "par_spl": [round(val[0][0], 2), round(val[0][1], 2)],
            "prf_usd": round(val[1], 2),
            "mnh_prf_usd": round(val[1] * 30, 2),
            "pwr_cons": round(val[4], 2),
            "mnh_pwr_cons": round(val[4] * 30, 2),
            "pwr_cons_usd": round(val[4] * data["elec"], 2),
            "mnh_pwr_cons_usd": round(val[4] * data["elec"] * 30, 2),
            "clear_prf_usd": round(val[1] - val[4] * data["elec"], 2),
            "mnh_clear_prf_usd": round(val[1] * 30 - val[4] * data["elec"] * 30, 2),
            "di": round(val[2], 2),
        })

    return duals

def make_table_asics(data: dict(), raw_profit: dict()):
    profit = dict()
    total = {
        "prf_usd": 0,
        "pwr_cons_usd": 0,
        "pwr_cons": 0,
        "clear_prf_usd": 0,
    }
    for m, l in raw_profit.items():
        profit[m.name] = []
        for coin, val in l.items():
            profit[m.name].append({
                "coin": coin.name,
                "hsh": f'{(round(val[0], 2))} Mh/s',
                "prf_coin": f'{(round(val[1], 2))} {coin.hashrate_no_code}',
                "mnh_prf_coin": f'{(round(val[1] * 30, 2))} {coin.hashrate_no_code}',
                "prf_usd": f'{(round(val[2], 2))} $',
                "mnh_prf_usd": f'{(round(val[2] * 30, 2))} $',
                "pwr_cons": f'{(round(val[3], 2))} kWh',
                "pwr_cons_usd": f'{(round(val[3] * data["elec"], 2))} $',
                "mnh_pwr_cons": f'{(round(val[3] * 30, 2))} kWh',
                "mnh_pwr_cons_usd": f'{(round(val[3] * 30 * data["elec"], 2))} $',
                "clear_prf_usd": f'{(round(val[2] - val[3] * data["elec"], 2))} $',
                "mnh_clear_prf_usd": f'{(round(val[2] * 30 - val[3] * data["elec"] * 30, 2))} $',
                "clear_prf_coin": f'{(round(val[1] - val[4], 2))} {coin.hashrate_no_code}',
                "mnh_clear_prf_coin": f'{(round(val[1] * 30 - val[4] * 30, 2))} {coin.hashrate_no_code}',
            })
        profit[m.name].sort(key=lambda a: float(a["clear_prf_usd"].split()[0]), reverse=True)
        total["prf_usd"] += float(profit[m.name][0]["prf_usd"].split()[0])
        total["pwr_cons_usd"] += float(profit[m.name][0]["pwr_cons_usd"].split()[0])
        total["pwr_cons"] += float(profit[m.name][0]["pwr_cons"].split()[0])
        total["clear_prf_usd"] += float(profit[m.name][0]["clear_prf_usd"].split()[0])\

    profit["Суммарная доходность конфигурации"] = [{
        "coin": "-",
        "hsh": "-",
        "prf_coin": "-",
        "mnh_prf_coin": "-",
        "prf_usd": f'{round(total["prf_usd"], 2)} $',
        "mnh_prf_usd": f'{round(total["prf_usd"] * 30, 2)} $',
        "pwr_cons": f'{round(total["pwr_cons"], 2)} kWh',
        "pwr_cons_usd": f'{round(total["pwr_cons_usd"], 2)} $',
        "mnh_pwr_cons": f'{round(total["pwr_cons"] * 30, 2)} kWh',
        "mnh_pwr_cons_usd": f'{round(total["pwr_cons_usd"] * 30, 2)} $',
        "clear_prf_usd":  f'{round(total["clear_prf_usd"], 2)} $',
        "mnh_clear_prf_usd": f'{round(total["clear_prf_usd"] * 30, 2)} $',
        "clear_prf_coin": "-",
        "mnh_clear_prf_coin": "-",
    }]

    return profit


def make_offer(config):
    return
