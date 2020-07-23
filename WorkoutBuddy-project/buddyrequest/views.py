from django.shortcuts import render
from buddyrequest.models import BuddyRequest

# Create your views here.
def database(request):
    buddyrequests=BuddyRequest.objects
    return render(request,'buddyrequest/database.html',{'buddyrequests':buddyrequests})

def profile(request):
    return render(request,'buddyrequest/profile.html')
def matches(request):
    #find post should forward here, not waiting
    return render(request,'buddyrequest/matches.html')
