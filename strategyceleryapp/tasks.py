# @Author: Chen yunsheng(Leo YS CHen)
# @Location: Taiwan
# @E-mail:leoyenschen@gmail.com
# @Date:   2017-02-14 00:11:27
# @Last Modified by:   Chen yunsheng

from StrategyCelery.celery import app
from .models import daily_price

@app.task
def hello_world():
    print('Hello World,fvf')

@app.task
def test_sqlite():
    print("test_sqlite")
    daily_prices = daily_price.objects.all()
    print(daily_prices)
    print("daily_prices['high_price']")
    print(daily_prices[0].high_price)


