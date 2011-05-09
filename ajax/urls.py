# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from authorization.forms import SigninUserForm, EditProfileForm

## Search
urlpatterns = patterns('ajax.views',
    url(r'^search$', "ajax_search", name="ajax_search_url"),    
)

## Authorization
urlpatterns += patterns('ajax.views',
    url(r"^signin/$", "validate", {"form_class": SigninUserForm}, name="signup_form_validate_url"),
    url(r"^profile/$", "validate_profile", {"form_class": EditProfileForm}, name="profile_validate_url"),
    url(r"^login/$", "validate_login", name="login_validate_url"),
    
    url(r"^get_signup_form/$", "get_signup_form", name="get_signup_form_url"),
    url(r"^get_login_form/$", "get_login_form", name="get_login_form_url"),
)