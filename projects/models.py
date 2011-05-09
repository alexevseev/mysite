# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import permalink

class ProjectTags(models.Model):
    name=models.CharField(max_length=50)    
    
    class Meta:
        ordering = ['name']
        
    def __unicode__(self):
        return self.name
        
class Projects(models.Model):
    title=models.CharField(max_length=250)    
    description = models.TextField( verbose_name =u"описание")   
    slug = models.SlugField(max_length=250, default='')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    tags=models.ManyToManyField(ProjectTags, related_name="projects")

    class Meta:
        verbose_name_plural = u"мои проекты"
        verbose_name = u"проект"

    def __unicode__(self):
        return self.title
    
    def showTags(self):
        tagsHTML = ""
        for projectTag in self.tags.all():
            tagsHTML += '<span style="background:#6D8DFF; font-size:14px">{0}</span><span> </span>'.format(projectTag.name)
        return tagsHTML
    showTags.allow_tags = True
    showTags.short_description = u'tags'    
    
    def getTagList(self):
        return [projectTag.name for projectTag in self.tags.all()]
    
    @permalink
    def get_absolute_url(self):
        return ('one_project_url', (self.slug,))

