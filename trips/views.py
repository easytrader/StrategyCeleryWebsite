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

# Create your views here.
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

def logout(request):
    auth.logout(request)
    messages.add_message(request, messages.INFO, "logout success")
    return redirect('/')

def strategy(request):
    Strategies = Strategy.objects.all()
    print(Strategies)

    if request.user.is_authenticated():
        username = request.user.username
        useremail = request.user.email
    messages.get_messages(request)

    template = get_template('strategy.html')
    request_context = RequestContext(request)
    request_context.push(locals())
    html = template.render(request_context)
    return HttpResponse(html)

@csrf_exempt
def strategy_del(request):
    if request.is_ajax():
        print("leo test strategy_del")
        print("checkedValue:")
        print(request.POST.get('checkedValue'))
        if request.POST.get('checkedValue') is not None:
            models.Strategy.objects.get(pk=request.POST.get('checkedValue')).delete()
        #template = get_template('strategy.html')
        #request_context = RequestContext(request)
        #request_context.push(locals())
        #html = template.render(request_context)
        #data = request.POST.get('checkedValue')
        return HttpResponse(json.dumps({'name': request.POST['checkedValue']}), content_type="application/json")
    else:
        raise Http404

def strategy_page(request, strategy_id):
    #print("leo test into strategy_page:strategy_id")
    strategy= models.Strategy.objects.get(pk=strategy_id)

    return render_to_response("strategy_page.html", {"strategy": strategy})

def new_strategy(request):
    return render_to_response('new_strategy.html', locals(), context_instance=RequestContext(request))

@csrf_exempt
def new_strategy_save(request):
    print("leo test new_strategy_save")
    print("request.POST")
    print(request.POST)
    print(request.POST['strategy_content'])
    if request.POST['strategy_content'] or request.POST['position_content'] or request.POST['name'] is not None:
        models.Strategy.objects.create(strategy_name=request.POST['name'],strategy=request.POST['strategy_content'],position=request.POST['position_content'],user=request.user)
    return HttpResponse("", content_type='application/json')

@csrf_exempt
def strategy_modify(request):
    print("leo test new_strategy_modify")
    print("request.POST['strategy_content']")
    print(request.POST['strategy_content'])
    #.update(field1='some value')
    if request.POST['strategy_content'] or request.POST['position_content'] or request.POST['name'] is not None:
        models.Strategy.objects.update(strategy=request.POST['strategy_content'],
                                       position=request.POST['position_content'])
    return HttpResponse("", content_type='application/json')

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
        print("request.method == 'POST' and request.is_ajax()")
        print(request.POST['strategy_content'])
        print("os.path.dirname")
        print(os.path.dirname(__file__))
        #os.path.join(os.path.dirname(__file__))


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

        ## call date command ##
        p = subprocess.Popen("python " + os.path.dirname(__file__)+"/../qstrader/strategy_backtest.py", stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        ## Wait for date to terminate. Get return returncode ##
        p_status = p.wait()
        print "Command output : ", output
        print "Command exit status/return code : ", p_status
        print "Command err : ", err

        #===========================================================
        f = open(os.path.dirname(__file__) + "/../qstrader/output.log", 'w')
        f.write(output)
        f.close()

        if err is None:
            err = ""
        f = open(os.path.dirname(__file__) + "/../qstrader/err.log", 'w')
        f.write(err)
        f.close()

        return HttpResponse(json.dumps({'name': request.POST['strategy_content']}), content_type="application/json")
    else:
        print("!request.method == 'POST' and request.is_ajax()")

        f = open(os.path.dirname(__file__) + "/../qstrader/output.log", "r")
        output = f.read()
        f.close()

        f = open(os.path.dirname(__file__) + "/../qstrader/err.log", "r")
        err = f.read()
        f.close()

        return render_to_response('strategy_run.html', locals())

