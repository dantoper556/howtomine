from django.db import models

# Create your models here.
class VideoCard(models.Model):
    name = models.CharField(max_length=60)
    hashrate_no_code = models.CharField(max_length=60)

    def __str__(self) -> str:
        return self.name

class CryptoCoin(models.Model):
    name = models.CharField(max_length=60)
    hashrate_no_code = models.CharField(max_length=60)
    
    def __str__(self) -> str:
        return self.name

class Asics(models.Model):
    name = models.CharField(max_length=60)
    hashrate_no_code = models.CharField(max_length=60)
    
    def __str__(self) -> str:
        return self.name
    
class Duals(models.Model):
    pair = models.ManyToManyField(CryptoCoin)

    def __str__(self) -> str:
        return f'{str(self.pair.all()[0])} + {str(self.pair.all()[1])}'