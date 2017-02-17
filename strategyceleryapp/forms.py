# @Author: Chen yunsheng(Leo YS CHen)
# @Location: Taiwan
# @E-mail:leoyenschen@gmail.com
# @Date:   2017-02-14 00:11:27
# @Last Modified by:   Chen yunsheng

from django import forms
from . import models
#from captcha.fields import CaptchaField

class LoginForm(forms.Form):
    username = forms.CharField(label='name', max_length=10)
    password = forms.CharField(label='password', widget=forms.PasswordInput())