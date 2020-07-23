from django.shortcuts import render

# Create your views here.
def requests(request):
    return render(request,'buddyrequest/database.html')

def profile(request):
    return render(request,'buddyrequest/profile.html')
