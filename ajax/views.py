# -*- coding: utf-8 -*-
from django.utils import simplejson
from django.http import HttpResponse
from django import forms
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings

from haystack.query import SearchQuerySet

from ajax.utils import LazyEncoder
from authorization.views import signin_user
from authorization.forms import SigninUserForm, EditProfileForm

def ajax_search(request):
    def make_result(obj):
        return [x.object.get_absolute_url(), x.object.title, x.object.title]
        
    if request.method == "GET":
        if request.GET.has_key('q'):
            query = request.GET['q']
            results = SearchQuerySet().filter(content=query)
            projects = { 'title':'Проекты',
                        'results':[make_result(x)  for x in results if x.model_name == 'projects'],
                        }
            services = { 'title':'Сервисы',
                        'results':[make_result(x)  for x in results if x.model_name == 'services'],
                        }
            out_data = [projects, services, ]
            return HttpResponse(simplejson.dumps(out_data), mimetype="application/json")

## VALIDATION ##
            
import time

def processErrors(request, form):
    if request.POST.getlist('fields'):
            fields = request.POST.getlist('fields') + ['__all__']
            errors = dict([(key, val) for key, val in form.errors.iteritems() if key in fields])
    else:
        errors = form.errors
    final_errors = {}
    for key, val in errors.iteritems():
        if key == '__all__':
            final_errors['__all__'] = val
        if not isinstance(form.fields[key], forms.FileField):
            html_id = form.fields[key].widget.attrs.get('id') or form[key].auto_id
            html_id = form.fields[key].widget.id_for_label(html_id)
            final_errors[html_id] = val
    data = {
        'valid': False,
        'errors': final_errors,
    }
    return data
    
def validate(request, *args, **kwargs):    
    form_class = kwargs.pop('form_class')    
    from_prefix = request.POST.get('formPrefix', '')
    form = form_class(request.POST, prefix=from_prefix)
    if form.is_valid():
        data = {
            'valid': True,
        }
        if request.POST.get('save'):
            signin_user(form)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
    else:        
        data = processErrors(request, form)
    json_serializer = LazyEncoder()
    time.sleep(1)
    return HttpResponse(json_serializer.encode(data), mimetype='application/json')
validate = require_POST(validate)

def validate_profile(request, *args, **kwargs):    
    if request.user.is_authenticated():
        form_class = kwargs.pop('form_class')
        edit_form = form_class(user=request.user, data=request.POST)
        if edit_form.is_valid():
            data = {
                'valid': True,
            }
            if request.POST.get('save'):
                user = edit_form.save() 
                request.user.message_set.create(message='Ваши данные обновлены')
        else:
            data = processErrors(request, edit_form)
    else:
        final_errors = {}
        final_errors['__all__'] = ["Вы не вошли",]
        data = {
            'valid': False,
            'errors': final_errors,
        }
        
    json_serializer = LazyEncoder()
    time.sleep(1)
    return HttpResponse(json_serializer.encode(data), mimetype='application/json')
validate_profile = require_POST(validate_profile)

def validate_login(request): 
    from_prefix = request.POST.get('formPrefix', '')
    if from_prefix:
        from_prefix += '-'
    username = request.POST.get(from_prefix+'username')
    password = request.POST.get(from_prefix+'password')
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            data = {
                'valid': True,
            }
    else:
        final_errors = {}
        final_errors['__all__'] = ["Имя или пароль неверные",]
        data = {
            'valid': False,
            'errors': final_errors,
        }
    json_serializer = LazyEncoder()
    time.sleep(1)
    return HttpResponse(json_serializer.encode(data), mimetype='application/json')
validate_login = require_POST(validate_login)

def ajax_logout(request):
    pass
    
def get_signup_form(request):
    signupForm = SigninUserForm(prefix=settings.PREFIX_SIGNUP)
    form = u"<div>{0}{1}</div>".format(signupForm['username'].label_tag(), signupForm['username'])
    form += u"<div>{0}{1}</div>".format(signupForm['password1'].label_tag(), signupForm['password1'])
    form += u"<div>{0}{1}</div>".format(signupForm['password2'].label_tag(), signupForm['password2'])
    form += u"<div>{0}{1}</div>".format(signupForm['email'].label_tag(), signupForm['email'])
    
    data={'form': form,}
    json_serializer = LazyEncoder()
    time.sleep(1)
    return HttpResponse(json_serializer.encode(data), mimetype='application/json')
    
def get_login_form(request):
    loginForm = AuthenticationForm(prefix=settings.PREFIX_LOGIN)
    form = u"<div>{0}{1}</div>".format(loginForm['username'].label_tag(), loginForm['username'])
    form += u"<div>{0}{1}</div>".format(loginForm['password'].label_tag(), loginForm['password'])
    
    data={'form': form,}
    json_serializer = LazyEncoder()
    time.sleep(1)
    return HttpResponse(json_serializer.encode(data), mimetype='application/json')