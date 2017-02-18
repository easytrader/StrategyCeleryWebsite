# @Author: Chen yunsheng(Leo YS CHen)
# @Location: Taiwan
# @E-mail:leoyenschen@gmail.com
# @Date:   2017-02-14 00:11:27
# @Last Modified by:   Chen yunsheng

from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
#import django.utils.timezone as timezone

# Create your models here.
class Strategy(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mod_date = models.DateTimeField(auto_now=True)
    strategy_name = models.CharField(max_length=20)
    strategy = models.TextField()
    position = models.TextField()


class symbol(models.Model):
    ticker = models.CharField(max_length=40)
    name = models.CharField(max_length=200)
    created_date = models.DateTimeField(auto_now=True)
    last_updated_date = models.DateTimeField(auto_now=True)

class daily_price(models.Model):
    symbol_id = models.IntegerField()
    price_date = models.DateTimeField()
    created_date = models.DateTimeField()
    last_updated_date = models.DateTimeField()
    open_price = models.DecimalField(max_digits=19, decimal_places=10)
    high_price = models.DecimalField(max_digits=19, decimal_places=10)
    low_price = models.DecimalField(max_digits=19, decimal_places=10)
    close_price = models.DecimalField(max_digits=19, decimal_places=10)
    adj_close_price = models.DecimalField(max_digits=19, decimal_places=10)
    volume = models.BigIntegerField()