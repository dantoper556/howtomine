from django.db import models

# Create your models here.
class VideoCard(models.Model):
    name = models.CharField(max_length=60)
    hashrate_no_code = models.CharField(max_length=60)