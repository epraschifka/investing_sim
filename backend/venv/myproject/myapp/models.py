from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from datetime import datetime
import json

# Create your models here.
class CustomUser(AbstractUser):
    portfolio_graph_default = {"date": [str(datetime.now())], "value": [0]}
    coins = models.ManyToManyField(to="Coin", through="Holding")
    money = models.DecimalField(max_digits=100, decimal_places=2, validators=[MinValueValidator(50)] )
    portfolio_graph = models.TextField(default=json.dumps(portfolio_graph_default))
    portfolio_value = models.DecimalField(max_digits=100, decimal_places=2)

class Holding(models.Model):
    coin = models.ForeignKey("Coin", on_delete=models.CASCADE)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1,validators=[MinValueValidator(1)])
    price_bought_at = models.DecimalField(decimal_places=10, max_digits=20)

class Coin(models.Model):
    graph_default = {"date": [], "value": []}
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
    graph = models.TextField(default=json.dumps(graph_default))