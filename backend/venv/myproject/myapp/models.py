from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Stock(models.Model):
    ticker = models.CharField(max_length=3)
    price = models.DecimalField(max_digits=100,decimal_places=2,default=1000000.00)
    quantity = models.IntegerField(default=0)

class User(AbstractUser):
    money = models.DecimalField(max_digits=100,decimal_places=2,default=1000000.00)
    stock = models.ForeignKey(Stock,on_delete=models.CASCADE,default=0)
