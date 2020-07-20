from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from buddyrequest.models import BuddyRequest
import pandas
def home(request):
    return render(request,'home.html')

@login_required(login_url='/accounts/signup')
def find(request):
    return render(request,'find.html')

@login_required(login_url='/accounts/signup')
def waiting(request):
    if request.method=='POST':
        #get data about USER
        userdatadf=pandas.read_csv('WorkoutBuddy\studentdata.csv',index_col=('netID'))
        netID=request.user.username
        userdata=userdatadf.loc[netID]
        name=userdata['name']
        major=userdata['major']
        year=userdata['year']
        rescollege=userdata['residentialcollege']
        days=request.POST.getlist('day')
        duration=request.POST['duration']
        workout_type=request.POST['workout_type']
        time_zone=request.POST['time_zone']
        group_size=request.POST['group_size']

        #list of data
        user_data_list=[name,days,duration,workout_type,time_zone,group_size]

        user_data_list_df=pandas.DataFrame(user_data_list)
        #list of requests in dataframe
        requestsList=list(BuddyRequest.objects.all().values())
        #dataframe of requests
        requestsdf=pandas.DataFrame(requestsList)
        print(requestsdf)
        #COMPARISION BETWEEN USER DATA AND REQUESTS ENTERED HERE


        #IF NO MATCH IS FOUND, ADD NEW REQUEST
        if match==False:
            req=BuddyRequest(name=name,major=major,year=year,rescollege=rescollege,days=days,duration=duration,
            workout_type=workout_type,time_zone=time_zone,group_size=group_size,user=request.user)
            req.save()
            return render(request,'waiting.html')

        #IF MATCH IS FOUND, GET DATA,  REMOVE IT FROM REQUESTS AND PUT IT IN A GROUP
        else:
            matchedName=name
            matchedRequest=BuddyRequest.objects.filter(name=matchedName)
            return render(request,'waiting.html',{'matched_person_name':matchedName})



@login_required(login_url='/accounts/signup')
def about(request):
    return render(request,'about.html')
