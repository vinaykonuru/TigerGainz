from django import template
from buddyrequest.models import BuddyRequest
from django.contrib.auth.models import User
import datetime
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
    request = BuddyRequest.objects.get(user = user)
    timedelta = datetime.datetime.now() - request.updated
    seconds = timedelta.total_seconds()
    print("Seconds" + seconds)
    seconds = 0
    SECONDS_IN_DAY = 86400
    if(seconds > SECONDS_IN_DAY):
        return True
    return False
