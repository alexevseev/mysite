from haystack.indexes import *
from haystack import site
from projects.models import Projects

class ProjectIndex(SearchIndex):
    text = CharField(document=True, use_template=True)

site.register(Projects, ProjectIndex)
