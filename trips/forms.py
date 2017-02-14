#_*_ encoding: utf-8 *_*
# @Author: Chen yunsheng(Leo YS CHen)
# @Date:   2017-02-14 00:11:27
# @Last Modified by:   Chen yunsheng

from django import forms
from . import models
#from captcha.fields import CaptchaField

class LoginForm(forms.Form):
    username = forms.CharField(label='姓名', max_length=10)
    password = forms.CharField(label='密碼', widget=forms.PasswordInput())