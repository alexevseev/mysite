# -*- coding: utf-8 -*-
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.conf import settings

from forms import ContactForm
from authorization.models import MyUser
from datetime import date

def get_my_age():    
    birthday = date(1985, 2, 6)
    now = date.today()
    age = now.year - birthday.year        
    if (now.month <= birthday.month and now.day < birthday.day and age > 0):
        ## day is less than birthday day in current year
        age -= 1
    ## get unit for years
    last_age_digit = age%10
    if last_age_digit == 1:
        unit = 'год'
    elif last_age_digit >= 2 and last_age_digit <= 4:
        unit = 'года'
    else:
        unit = 'лет'    
    return "{0} {1}".format(age, unit)
    
def show_about(request):
    if request.method == "POST":
        copyRequest = request.POST.copy()
        if request.user.is_authenticated():
            ## in case of user is logged in, username and email fields are not shown
            ## get username and email from database
            user = MyUser.objects.get(username = request.user)
            copyRequest['name'] = user.username
            copyRequest['email'] = user.email
        form = ContactForm(copyRequest)
        if form.is_valid():
            recipients = [settings.ADMINS[0][1], ]            
            name = form.cleaned_data['name']
            subject = "Mysite message from {0}".format(name)            
            message = form.cleaned_data['message']
            sender = form.cleaned_data['email']
            messages.success(request, "Сообщение отправлено")
            send_mail(subject, message, sender, recipients)
            return HttpResponseRedirect(reverse('thankyou_url')) # Redirect after POST
        else:
            pass
    else:
        form = ContactForm()    
    template_context =  {'form':form, 'my_age':get_my_age(),}
    return render_to_response('about/form.html', template_context, RequestContext(request))
    
def show_thankyou(request):
    template_context = {}
    return render_to_response('about/thankyou.html', template_context, RequestContext(request))