# -*- coding: utf-8 -*-
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from django.conf import settings

from forms import ContactForm
from authorization.models import MyUser

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
            return redirect("about_url")
        else:
            pass
    else:
        form = ContactForm()
    
    template_context =  {'form':form}
    return render_to_response('about/form.html', template_context, RequestContext(request))