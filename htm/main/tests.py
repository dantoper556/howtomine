from django.test import TestCase
from .calculators import calc_config_profit
from .models import *
from .presenters import make_table_vc

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


