# StrategyCeleryWebsite

username: `leo` <br/>
password: `qweasdzxc`

```bash
$ mkdir github
$ cd github
$ git clone https://github.com/easytrader/StrategyCeleryWebsite.git
$ pip install -r https://raw.githubusercontent.com/easytrader/StrategyCeleryWebsite/master/requirements.txt
$ sudo pip install celery
$ sudo pip install celery-with-redis
$ sudo apt install redis-server
$ sudo pip install django-celery
$ sudo pip install apscheduler
$ cd StrategyCeleryWebsite
$ python manage.py runserver
```
*****************************************************************************************************************
I have modified the qstrader. You should use my qstrader code.
```bash
$ git clone https://github.com/easytrader/qstrader.git
$ cd qstrader
$ uninstall -- sudo pip uninstall qstrader
$ install -- sudo python setup.py install
```
*****************************************************************************************************************
![alt tag](https://github.com/easytrader/StrategyCeleryWebsite/blob/master/monthly.png)
![alt tag](https://github.com/easytrader/StrategyCeleryWebsite/blob/master/monthly_result_1.png)
![alt tag](https://github.com/easytrader/StrategyCeleryWebsite/blob/master/monthly_result_2.png)
*****************************************************************************************************************

20170614- add new feature, running specific strategy on specific time everyday. It can be added jobs on the fly.
