#_*_ encoding: utf-8 *_*
from django import forms
from . import models
#from captcha.fields import CaptchaField

class LoginForm(forms.Form):
    username = forms.CharField(label='姓名', max_length=10)
    password = forms.CharField(label='密碼', widget=forms.PasswordInput())