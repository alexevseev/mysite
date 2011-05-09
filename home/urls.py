from django.conf.urls.defaults import *

urlpatterns = patterns('home.views',
    url(r'^$', 'show_home', name='root_url'),
)
