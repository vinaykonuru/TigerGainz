from django import template
from buddyrequest.models import BuddyRequest
from django.contrib.auth.models import User

register = template.Library()

@register.filter
def check_requests(user):
    requestsList=BuddyRequest.objects.all()
    for entry in requestsList:
        if entry.user==user:
            return True
    return False
