# -*- coding: utf-8 -*-
## django imports
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

## custom imports
from authorization.forms import SigninUserForm, EditProfileForm

def signin_user(form):
    user = form.save()
    # No other confirmation is required for signing in ...
    # To confirm by email, first step is to set here 'is_active = False'
    user.is_active = True
    user.email = form.cleaned_data['email']
    user.save()  
    
def show_login_page(request, auth_form=None):
    if auth_form == None:
        auth_form = AuthenticationForm()
    template_context = {"form": auth_form, }
    return render_to_response("authorization/login_page.html", template_context, RequestContext(request))
    
def show_signin_page(request, signin_form=None):    
    if signin_form == None:
        signin_form = SigninUserForm()        
    template_context = {"form": signin_form, } 
    return render_to_response("authorization/signin_page.html", template_context, RequestContext(request))
    
def show_signin_result(request):   
    if request.POST:
        signin_form = SigninUserForm(request.POST)
        if signin_form.is_valid(): 
            signin_user(signin_form)
            return render_to_response("authorization/signin_passed_page.html", {}, RequestContext(request))
        else:    
            return show_signin_page(request, signin_form)  
    return show_signin_page(request)
    
def show_login_result(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # Redirect to a success page
                return render_to_response("authorization/login_passed_page.html", {}, RequestContext(request))
            else:
                # Return a 'disabled account' error message
                return render_to_response("authorization/login_failed_page.html", {}, RequestContext(request))
        else:
            auth_form = AuthenticationForm()
            auth_form.errors.update({u'': u'Имя или пароль неверные'})
            return show_login_page(request, auth_form)
    return show_login_page(request)
    
@login_required
def show_logout_page(request):
    logout(request)
    return render_to_response("authorization/logout_page.html", {}, RequestContext(request))
    
@login_required
def show_editprofile_page(request):
    if request.method == 'POST':
        edit_form = EditProfileForm(user=request.user, data=request.POST)
        if edit_form.is_valid():
            user = edit_form.save()
            request.user.message_set.create(message='Ваши данные обновлены')
            return HttpResponseRedirect('.')
    if request.method == 'GET':
        edit_form = EditProfileForm(user = request.user)
        
    template_context = {'form':edit_form}
    return render_to_response('authorization/edit_profile.html', template_context, RequestContext(request))