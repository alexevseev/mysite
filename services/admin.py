# -*- coding: utf-8 -*-
from django.contrib import admin
from services.models import Services

class ServicesAdmin(admin.ModelAdmin):
    prepopulated_fields = { 'slug': ['title'] }
    list_display = ('title', 'short_description')
    list_display_links = ('short_description',)  

admin.site.register(Services, ServicesAdmin)