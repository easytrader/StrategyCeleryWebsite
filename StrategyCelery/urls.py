"""UseradminTest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from strategyceleryapp.views import index,login,logout,strategy,new_strategy,strategy_page,strategy_del,new_strategy_save,strategy_modify,strategy_run

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', index),
    url(r'^login/$', login),
    url(r'^logout/$', logout),
    url(r'^strategy/$', strategy),
    url(r'^strategy/del/$', strategy_del),
    url(r'^strategy/(?P<strategy_id>[0-9]+)', strategy_page, name="strategy_page"),
    url(r'^new_strategy/$', new_strategy),
    url(r'^new_strategy_save/$', new_strategy_save),
    url(r'^strategy_modify/$', strategy_modify),
    url(r'^strategy_run/$', strategy_run),
    #url(r'^test/$', test_InsertSP500symbols),
]