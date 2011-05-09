# -*- coding: utf-8 -*-
from django.contrib import admin
from django.db import models
from projects.models import Projects, ProjectTags

class ProjectTagsAdmin(admin.ModelAdmin):
    # following method is needed to hide model from root admin page
    # for this purpose also in index.html for admin page 'if' condition is insert
    def get_model_perms(self, *args, **kwargs):
        perms = admin.ModelAdmin.get_model_perms(self, *args, **kwargs)
        perms['list_hide'] = True
        return perms
    
class ProjectsAdmin(admin.ModelAdmin):
    prepopulated_fields = { 'slug': ['title'] }
    list_display = ('title', 'showTags')
    list_display_links = ('title',)  

admin.site.register(Projects, ProjectsAdmin)
admin.site.register(ProjectTags, ProjectTagsAdmin)