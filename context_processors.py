import sys
import django
import settings

def DjangoVersionContextProcessor(request):
    one, two, three, four, five = django.VERSION
    return {"DJANGO_VERSION": "%s.%s.%s" % (one, two, three)}

def PythonVersionContextProcessor(request):
    one, two, three, four, five = sys.version_info
    return {"PYTHON_VERSION": "%s.%s.%s" % (one, two, three)}

