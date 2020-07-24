from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from buddyrequest.models import BuddyRequest
import pandas
import csv
from .matching_algorithm import get_matches
# Create your views here.

@login_required(login_url='/accounts/signup')
def database(request):
    buddyrequests=BuddyRequest.objects
    return render(request,'buddyrequest/database.html',{'buddyrequests':buddyrequests})

@login_required(login_url='/accounts/signup')
def profile(request):
    return render(request,'buddyrequest/profile.html')

@login_required(login_url='/accounts/signup')
def matches(request):
    if request.method=='POST':
        #get data about USER
        userdatadf=pandas.read_csv('WorkoutBuddy\studentdata.csv',index_col=('netID'))
        netID=request.user.username
        try:
            userdata=userdatadf.loc[netID]
        except KeyError:
            print('netID wasn\'t found in csv')
        name=userdata['name']
        major=userdata['major']
        year=userdata['year']
        rescollege=userdata['residentialcollege']
        days=request.POST.getlist('day')
        duration=request.POST['duration']
        workout_type=[]
        workout_type.append(request.POST['workout_type'])
        time_zone=request.POST['time_zone']
        group_size=request.POST['group_size']
        profile_picture=request.POST['profile_picture']
        user=request.user
        #list of data
        user_data_list=[netID,name,major,year,rescollege,profile_picture,days,duration,workout_type,time_zone,group_size]
        #list of requests in dataframe
        requestsList=list(BuddyRequest.objects.all().values())
        matched_people=get_matches(user_data_list, requestsList)
        if len(requestsList) < 1 or matched_people==[]:
            req=BuddyRequest(netID=netID,name=name,major=major,year=year,rescollege=rescollege,profile_picture=profile_picture,
            days=days,duration=duration,workout_type=workout_type,time_zone=time_zone,group_size=group_size,user=user)
            req.save()
            return render(request,'buddyrequest/matches.html')

        print('WE REACHED THE END')
        matched=True
        if len(matched_people) == 0:
            matched=False
        return render(request,'buddyrequest/matches.html',{'matched_people':matched_people,"matched":matched})
