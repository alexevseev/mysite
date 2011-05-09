# -*- coding: utf-8 -*-
from services.models import Services

def get_latest_service():   
    try:
        latest_service = Services.objects.order_by('-created')[0]
    except IndexError:
        latest_service = None
    return latest_service
