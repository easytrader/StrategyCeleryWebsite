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
#===================
import datetime
import lxml.html
from urllib2 import urlopen
#==================
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
    return render_to_response('new_strategy.html', locals(), context_instance=RequestContext(request))

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
def strategy_run(request):
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

        p = subprocess.Popen("python " + os.path.dirname(__file__) + "/../qstrader/strategy_backtest.py", stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=True)
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

def obtain_parse_wiki_snp500():
    """Download and parse the Wikipedia list of S\&P500
    constituents using requests and libxml.

    Returns a list of tuples for to add to MySQL."""

    # Stores the current time, for the created_at record
    now = datetime.datetime.utcnow()

    # Use libxml to download the list of S\&P500 companies and obtain the symbol table
    page = lxml.html.parse(urlopen('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'))
    # symbolslist = page.xpath('//table[2]/tr')[1:]
    symbolslist = page.xpath('//table[1]/tr')[1:]

    # Obtain the symbol information for each row in the S\&P500 constituent table
    symbols = []
    for symbol in symbolslist:
        tds = symbol.getchildren()

        sd = {'ticker': tds[0].getchildren()[0].text,
                'name': tds[1].getchildren()[0].text,
                'sector': tds[3].text}
        # Create a tuple (for the DB format) and append to the grand list
        symbols.append((sd['ticker'], 'stock', sd['name'],
                        sd['sector'], 'USD', now, now))

    return symbols

"""
def test_InsertSP500symbols(request):
    symbols = obtain_parse_wiki_snp500()
    for symbol in symbols:
        models.symbol.objects.create(ticker=symbol[0], instrument=symbol[1], name=symbol[2], sector=symbol[3], currency=symbol[4])
"""
