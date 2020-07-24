from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from buddyrequest.models import BuddyRequest
from partners.models import Partners
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

def partner_match(request,partner_id):
    print(partner_id)
    if request.method=="POST":
        #partner object for current user
        user_request=BuddyRequest.objects.get(user=request.user)
        matched_user=User.objects.get(pk=partner_id)
        partner_request=BuddyRequest.objects.get(user=matched_user)

        partner_user=Partners()
        partner_user.netID=user_request.netID
        partner_user.name=user_request.name
        partner_user.major=user_request.major
        partner_user.rescollege=user_request.rescollege
        partner_user.profile_picture=user_request.profile_picture
        partner_user.days=user_request.days
        partner_user.duration=user_request.duration
        partner_user.workout_type=user_request.workout_type
        partner_user.time_zone=user_request.time_zone
        partner_user.group_size=user_request.group_size
        partner_user.user=request.user
        partner_user.partner=partner_request.user
        partner_user.save()

        #partner object for matched user
        partner_match=Partners()
        partner_match.netID=partner_request.netID
        partner_match.name=partner_request.name
        partner_match.major=partner_request.major
        partner_match.rescollege=partner_request.rescollege
        partner_match.profile_picture=partner_request.profile_picture
        partner_match.days=partner_request.days
        partner_match.duration=partner_request.duration
        partner_match.workout_type=partner_request.workout_type
        partner_match.time_zone=partner_request.time_zone
        partner_match.group_size=partner_request.group_size
        partner_match.user=partner_request.user
        partner_match.partner=request.user
        partner_match.save()
        #delete partner and user requests from database
        user_request.delete()
        partner_request.delete()
        return redirect('/partners')
@login_required(login_url='/accounts/signup')
def matches(request):
    if request.method=='POST':
        #if the user already has a request in the database, go back to home page
        requestsList=list(BuddyRequest.objects.all().values())
        for entry in requestsList:
            print(request.user)
            if request.user.id==(entry['user_id']):
                return redirect('home')
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
        #put this after search for matches so user doesn't match with themselves
        req_user=BuddyRequest(netID=netID,name=name,major=major,year=year,rescollege=rescollege,profile_picture=profile_picture,
        days=days,duration=duration,workout_type=workout_type,time_zone=time_zone,group_size=group_size,user=user)
        req_user.save()
        if len(requestsList) < 1:
            return render(request,'buddyrequest/matches.html')
        else:
            matched_people=get_matches(user_data_list, requestsList)

            if matched_people==[]:
                return render(request,'buddyrequest/matches.html')

        print('WE REACHED THE END')
        matched=True
        if len(matched_people) == 0:
            matched=False
        return render(request,'buddyrequest/matches.html',{'matched_people':matched_people,"matched":matched})
