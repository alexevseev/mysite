# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import permalink
from django.conf import settings

multithreaded_server=True
if settings.LOCAL:
    multithreaded_server=False

class Services(models.Model):
    title=models.CharField(max_length=250)    
    full_description_url=models.URLField(verify_exists=multithreaded_server, max_length=250)    
    short_description = models.CharField(max_length=250, verbose_name =u"краткое описание")   
    slug = models.SlugField(max_length=250, default='')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = u"сервисы"
        verbose_name = u"сервис"

    def __unicode__(self):
        return self.title
    
    @permalink
    def get_absolute_url(self):
        return ('service_url', (self.slug,))

