from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    coins = models.ManyToManyField(to="Coin", through="Holding")
    money = models.DecimalField(max_digits=100, decimal_places=2, default=1000000.00)

class Holding(models.Model):
    coin = models.ForeignKey("Coin", on_delete=models.CASCADE)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    quantity = models.IntegerField()

class Coin(models.Model):
    symbol = models.CharField(max_length=3)
    name = models.CharField(max_length=100)
    image_url = models.CharField(max_length=256)
    price = models.DecimalField(max_digits=15,decimal_places=10)
    market_cap = models.DecimalField(max_digits=20,decimal_places=2)
    volume = models.IntegerField()
    high_24h = models.DecimalField(max_digits=20,decimal_places=2)
    low_24h = models.DecimalField(max_digits=20,decimal_places=2)
    change_24h = models.DecimalField(max_digits=20,decimal_places=2)
    percent_change_24h = models.DecimalField(max_digits=20,decimal_places=2)
