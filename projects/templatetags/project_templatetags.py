from django import template
register = template.Library()

def getDictItem ( item, string ):
    if isinstance(item, dict):
        return item.get(string)
    else:
        return None
    
register.filter(getDictItem)

## django filter examples:
##     django/template/defaultfilters.py 
## django tags examples:
##     django/template/defaulttags.py.