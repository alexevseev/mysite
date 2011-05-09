# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from authorization.forms import SigninUserForm, EditProfileForm

urlpatterns = patterns('authorization.views',
    url(r'^login/$', 'show_login_page', name='login_page_url'),
    url(r'^logout/$', 'show_logout_page', name='logout_page_url'),
    url(r'^signin/$', 'show_signin_page', name='signin_page_url'),
    url(r'^login_pass/$', 'show_login_result',  name='login_result_url'),
    url(r'^signin_pass/$', 'show_signin_result',  name='signin_result_url'),
    url(r'^edit_profile/$', 'show_editprofile_page',  name='edit_profile_url'),
)