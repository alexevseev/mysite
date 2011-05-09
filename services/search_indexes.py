from haystack.indexes import *
from haystack import site
from services.models import Services

class ServiceIndex(SearchIndex):
    text = CharField(document=True, use_template=True)

site.register(Services, ServiceIndex)
