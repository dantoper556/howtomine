from django.test import TestCase
from .calculators import calc_config_profit
from .models import *
from .presenters import make_table_vc

class test1(TestCase):
    def setUp(self) -> None:
        self.config = dict()
        print(VideoCard.objects.all())
        for el in VideoCard.objects.all():
            
            if (el.hashrate_no_code == "2060s"):
                self.config[el] = 10
        self.data = dict()
        self.data["elec"] = 0.1
        print(self.config)
        
        
    
    def test(self):
        ret = calc_config_profit(self.config, self.data["elec"])
        tbl = make_table_vc(self.data, ret)
        ans1 = "0 $"
        self.assertEqual(self.config, ans1)


