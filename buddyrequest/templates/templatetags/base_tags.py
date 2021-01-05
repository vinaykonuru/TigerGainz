from django import template
from buddyrequest.models import BuddyRequest
from django.contrib.auth.models import User

register = template.Library()

#check if the user has made a request
@register.filter
def check_requests(user):
    requestsList=BuddyRequest.objects.all()
    for entry in requestsList:
        if entry.user==user:
            return True
    return False

#check if the current user has a partner other than himself
@register.filter
def check_partner(user):
    requestsList=BuddyRequest.objects.all()
    for entry in requestsList:
        if entry.partner==user:
            return True
    return False
