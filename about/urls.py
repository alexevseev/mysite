from django.conf.urls.defaults import *

urlpatterns = patterns('about.views',
    url(r'^$', 'show_about', name='about_url'),
    url(r'^thankyou/$', 'show_thankyou', name='thankyou_url'),
)
