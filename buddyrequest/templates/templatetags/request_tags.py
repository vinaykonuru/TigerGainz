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
# returns true is more than 24 hours have passed since making connection
@register.filter
def check_time(user):
    print('Time class')
    request = BuddyRequest.objects.get(user = user)
    time = request.updated.date()
    print(time)
    if(time.hour * 3600 + time.minute * 60 + time.second > 86400):
        return True
    return False
