# @Author: Chen yunsheng(Leo YS CHen)
# @Location: Taiwan
# @E-mail:leoyenschen@gmail.com
# @Date:   2017-02-14 00:11:27
# @Last Modified by:   Chen yunsheng

from django.template import RequestContext
from django.template.loader import get_template
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.shortcuts import redirect,render_to_response
from django.contrib import messages
from . import models, forms

from django.contrib.auth import authenticate
from django.contrib import auth
from .models import Strategy
from django.views.decorators.csrf import csrf_exempt
import json
import subprocess
import os

import datetime
import urllib2
import  threading

"""
index.html's view function
"""
def index(request, pid=None, del_pass=None):

    if request.user.is_authenticated():
        username = request.user.username
        useremail = request.user.email
    messages.get_messages(request)

    template = get_template('index.html')
    request_context = RequestContext(request)
    request_context.push(locals())
    html = template.render(request_context)
    return HttpResponse(html)

"""
login.html's view function
"""
@csrf_exempt
def login(request):

    if request.user.is_authenticated():
        return redirect('/')

    if request.method == 'POST':
        login_form = forms.LoginForm(request.POST)
        if login_form.is_valid():
            login_name=request.POST['username'].strip()
            login_password=request.POST['password']
            user = authenticate(username=login_name, password=login_password)
            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    messages.add_message(request, messages.SUCCESS, 'login successful')
                    return redirect('/')
                else:
                    messages.add_message(request, messages.WARNING, 'account cant use')
            else:
                messages.add_message(request, messages.WARNING, 'login fail')
        else:
            messages.add_message(request, messages.INFO,'Please check input content')
    else:
        login_form = forms.LoginForm()

    template = get_template('login.html')
    request_context = RequestContext(request)
    request_context.push(locals())
    html = template.render(request_context)
    return HttpResponse(html)

"""
logout.html's view function
"""
def logout(request):
    auth.logout(request)
    messages.add_message(request, messages.INFO, "logout success")
    return redirect('/')

"""
strategy.html's view function
"""
def strategy(request):
    Strategies = Strategy.objects.all()

    if request.user.is_authenticated():
        username = request.user.username
        useremail = request.user.email
    messages.get_messages(request)

    template = get_template('strategy.html')
    request_context = RequestContext(request)
    request_context.push(locals())
    html = template.render(request_context)
    return HttpResponse(html)

"""
strategy.html del button's function
"""
@csrf_exempt
def strategy_del(request):
    if request.is_ajax():
        if request.POST.get('checkedValue') is not None:
            models.Strategy.objects.get(pk=request.POST.get('checkedValue')).delete()

        return HttpResponse(json.dumps({'name': request.POST['checkedValue']}), content_type="application/json")
    else:
        raise Http404


"""
strategy_page.html's view function
"""
def strategy_page(request, strategy_id):
    strategy= models.Strategy.objects.get(pk=strategy_id)

    return render_to_response("strategy_page.html", {"strategy": strategy})

"""
new_strategy_page.html's view function
"""
def new_strategy(request):
    return render_to_response('new_strategy.html', {})

"""
new_strategy_page.html save strategy's function
"""
@csrf_exempt
def new_strategy_save(request):
    if request.POST['strategy_content'] or request.POST['position_content'] or request.POST['name'] is not None:
        models.Strategy.objects.create(strategy_name=request.POST['name'],strategy=request.POST['strategy_content'],position=request.POST['position_content'],user=request.user)
    return HttpResponse("", content_type='application/json')

"""
strategy_page.html save strategy's function
"""
@csrf_exempt
def strategy_modify(request):
    if request.POST['strategy_content'] or request.POST['position_content'] or request.POST['name'] is not None:
        models.Strategy.objects.filter(pk=request.POST['pk_key']).update(strategy=request.POST['strategy_content'],
                                       position=request.POST['position_content'])
    return HttpResponse("", content_type='application/json')

"""
strategy_page.html run strategy's button
"""
@csrf_exempt
def strategy_run(request, strategy_id):
    print("leo test strategy_run")
    if request.user.is_authenticated():
        username = request.user.username
        useremail = request.user.email
    messages.get_messages(request)

    print(request.POST)

    template = get_template('strategy_run.html')
    request_context = RequestContext(request)
    request_context.push(locals())
    html = template.render(request_context)

    if request.method == 'POST' and request.is_ajax():

        if not request.POST['tickers'] or not request.POST['begin_date'] or not request.POST['end_date']:
            print("tickers is None")
            return HttpResponse("", content_type="application/json")

        f = open(os.path.dirname(__file__)+"/../qstrader/custom_strategy.py", 'w')
        f.write(request.POST['strategy_content'])
        f.close()

        f = open(os.path.dirname(__file__) + "/../qstrader/custom_position.py", 'w')
        f.write(request.POST['position_content'])
        f.close()


        png_file = os.path.dirname(__file__)+"/../static/img/backtest_result.png"

        ## delete only if file exists ##
        if os.path.exists(png_file):
            os.remove(png_file)
        else:
            print("Sorry, I can not remove %s file." % png_file)

        cmd = "python " + os.path.dirname(__file__) + "/../qstrader/strategy_backtest.py %s %s %s" % (request.POST['tickers'].encode("utf8"),request.POST['begin_date'],request.POST['end_date'])
        print("cmd")
        print(cmd)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        ## Wait for date to terminate. Get return returncode ##
        p_status = p.wait()
        print "Command output : ", output
        print "Command exit status/return code : ", p_status
        print "Command err : ", err

        #===========================================================

        strategy_output = models.strategy_output.objects.filter(user__username=request.user)

        if not strategy_output.exists():
            #print("strategy_output is empty")
            models.strategy_output.objects.create(strategy_output=output, strategy_error=err, user= request.user)
        else:
            #print("strategy_output is not empty")
            models.strategy_output.objects.filter(user__username=request.user).update(strategy_output=output, strategy_error=err)


        return HttpResponse(json.dumps({'name': request.POST['strategy_content']}), content_type="application/json")
    else:
        print("!request.method == 'POST' and request.is_ajax()")

        strategy_output = models.strategy_output.objects.get(user__username=request.user)
        output = strategy_output.strategy_output
        err = strategy_output.strategy_error

        return render_to_response('strategy_run.html', locals())

"""
running job.html's view function
"""
def running_jobs(request):
    #Strategies = Strategy.objects.all()

    if request.user.is_authenticated():
        username = request.user.username
        useremail = request.user.email
    messages.get_messages(request)

    template = get_template('strategy.html')
    request_context = RequestContext(request)
    request_context.push(locals())
    html = template.render(request_context)

    running_jobs = scheduler.get_jobs()
    #running_jobs = []

    today = datetime.datetime.now()
    #return HttpResponse(html)
    return render_to_response('running_jobs.html', {"running_jobs": running_jobs, "username":username, "today":today},
                              context_instance=RequestContext(request))

#initial apscheduler
from apscheduler.schedulers.background import BackgroundScheduler
from pytz import utc
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

jobstores = {

    'default': SQLAlchemyJobStore(url='sqlite:///db.sqlite3')
}
executors = {
    'default': ThreadPoolExecutor(20),
    'processpool': ProcessPoolExecutor(5)
}
job_defaults = {
    'coalesce': False,
    'max_instances': 3
}
scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=utc)
scheduler.start()


lock = threading.Lock()

def job(strategy, userid, start_date):
    #print("leo test strategy:"+strategy)
    lock.acquire()
    print("===================leo test job start==========================")
    # ====================================

    f = open(os.path.dirname(__file__) + "/../qstrader/custom_strategy.py", 'w')
    f.write(strategy.strategy)
    f.close()

    f = open(os.path.dirname(__file__) + "/../qstrader/custom_position.py", 'w')
    f.write(strategy.position)
    f.close()

    png_file = os.path.dirname(__file__) + "/../static/img/backtest_result.png"

    ## delete only if file exists ##
    if os.path.exists(png_file):
        os.remove(png_file)
    else:
        print("Sorry, I can not remove %s file." % png_file)

    input_tickers = strategy.tickers.encode("utf8")

    today = datetime.date.today()
    # print("today:"+today)

    cmd = "python " + os.path.dirname(__file__) + "/../qstrader/strategy_backtest.py %s %d %s %s %s" % (
        input_tickers, userid, strategy.strategy_name, start_date, today)
    print("cmd")
    print(cmd)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    ## Wait for date to terminate. Get return returncode ##
    p_status = p.wait()
    print "Command output : ", output
    print "Command exit status/return code : ", p_status
    print "Command err : ", err

    # ====================================
    # ===========================================================

    # ===========================================================

    strategy_output = models.strategy_output.objects.filter(user_id=userid,
                                                            strategy_name=strategy.strategy_name)

    print("leo test strategy_output:")

    if not strategy_output.exists():
        # print("strategy_output is empty")
        models.strategy_output.objects.create(strategy_output=output, strategy_name=strategy.strategy_name,
                                              strategy_error=err, user_id=userid)
    else:
        # print("strategy_output is not empty")
        models.strategy_output.objects.filter(user_id=userid, strategy_name=strategy.strategy_name).update(
            strategy_output=output, strategy_error=err, mod_date=datetime.datetime.now())
    # ============================================================================
    print("===================leo test job end==========================")
    lock.release()

"""
strategy_page.html daily run strategy's button
"""
def daily_run_strategy(request):
    print("daily_run_strategy")

    strategy = models.Strategy.objects.get(pk=request.POST['strategy_id'])
    full_id = request.user.username + strategy.strategy_name
    print("full_id: "+full_id)
    today = datetime.date.today()
    one_month_ago = datetime.date.today() - datetime.timedelta(days=60)
    #scheduler.add_job(job, 'interval', id=full_id, args=[strategy,'world'], seconds=30)
    scheduler.add_job(job, 'cron', id=full_id, args=[strategy, request.user.id, one_month_ago], day_of_week='0-5', hour='6', minute='30')
    return HttpResponse("", content_type='application/json')

"""
strategy_page.html delete daily run strategy's button
"""
def del_daily_run_strategy(request):
    print("del daily_run_strategy")
    strategy = models.Strategy.objects.get(pk=request.POST['strategy_id'])
    full_id = request.user.username + strategy.strategy_name
    print("full_id: " + full_id)
    scheduler.remove_job(full_id)
    return HttpResponse("", content_type='application/json')

@csrf_exempt
def aps_del(request):
    #print("leo test in aps del")

    if request.is_ajax():
        print("leo test in aps del")
        if request.POST.get('job-id') is not None:
            #print("job del:"+request.POST.get('job-id'))
            jobid = request.POST.get('job-id')
            scheduler.remove_job(jobid)

        return HttpResponse(json.dumps({'name': ""}), content_type="application/json")
    else:
        raise Http404
