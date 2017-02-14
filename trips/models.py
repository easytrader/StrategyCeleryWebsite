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


