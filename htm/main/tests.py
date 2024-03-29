from django.test import TestCase
from .calculators import calc_config_profit, calc_asics_config_profit
from .models import *
from .presenters import make_table_vc, make_table_asics
import json

class test1(TestCase):
    def setUp(self) -> None:
        self.config = dict()
        VideoCard.objects.create(name="RTX 3070", hashrate_no_code="3070")
        for el in VideoCard.objects.all():
            
            if (el.hashrate_no_code == "3070"):
                self.config[el] = 10
        self.data = dict()
        self.data["elec"] = 0.1

    def test(self):
        VideoCard.objects.create(name="RTX 3070", hashrate_no_code="3070")
        CryptoCoin.objects.create(name="Conflux", hashrate_no_code="CFX")
        ret = calc_config_profit(self.config, self.data["elec"])
        tbl = make_table_vc(self.data, ret)
        
        self.assertTrue(abs(float(tbl[0]["hsh"].split()[0]) / (579.2) - 1) < 0.01)
        self.assertTrue(abs(float(tbl[0]["pwr_cons"].split()[0]) / (140 * 10 * 24 / 1000) - 1) < 0.05)

class test2(TestCase):
    def setUp(self) -> None:
        self.config = dict()
        Asics.objects.create(name="JASMINER X16-Q", hashrate_no_code="x16q")
        for el in Asics.objects.all():
            if (el.hashrate_no_code == "x16q"):
                self.config[el] = 10
        self.data = dict()
        self.data["elec"] = 0.1

    def test(self):
        Asics.objects.create(name="JASMINER X16-Q", hashrate_no_code="x16q")
        CryptoCoin.objects.create(name="Ethereum Classic", hashrate_no_code="ETC")
        ret = calc_asics_config_profit(self.config, self.data["elec"])
        tbl = make_table_asics(self.data, ret)
        
        self.assertTrue(abs(float(tbl['JASMINER X16-Q'][0]['hsh'].split()[0]) / (1.95 * 10) - 1) < 0.01)
        self.assertTrue(abs(float(tbl['JASMINER X16-Q'][0]['pwr_cons'].split()[0]) / (15.1 * 10) - 1) < 0.01)


class test3(TestCase):
    def setUp(self) -> None:
        pass

    def test(self):
        f1 = open("./main/jsons/coins.json")
        dat = json.load(f1)
        self.assertTrue(abs(dat["parsed"]["Conflux"]["usd_per_coin"] - 0.16756) < 0.001)
        



