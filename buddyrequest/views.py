from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from buddyrequest.models import BuddyRequest
from datetime import datetime
import pandas
import csv
from .email import mail
from .matching_algorithm import get_matches
from .tigerhub_access import getStudentInfo
# Create your views here.

@login_required(login_url='/accounts/login')
def database(request):
    buddyrequests=BuddyRequest.objects.all()
    workout_type_filter = request.POST.getlist('workout_type_filter')
    duration_filter = request.POST.getlist('duration_filter')
    time_zone_filter = request.POST.getlist('time_zone_filter')
    location_filter = request.POST.getlist('location_filter')
    if(workout_type_filter == ['']):
        workout_type_filter = []
    if(duration_filter == ['']):
        duration_filter = []
    if(time_zone_filter == ['']):
        time_zone_filter = []
    if(location_filter == ['']):
        location_filter = []
    workout_type_filter_set = set(workout_type_filter)
    duration_filter_set = set(duration_filter)
    time_zone_filter_set = set(time_zone_filter)
    location_filter_set = set(location_filter)
    profiles = []
    for entry in buddyrequests:
        if(entry.partner == None and entry.user != request.user):
            duration = entry.duration.strip('][\ '')
            timezone = entry.time_zone.strip('][\' ')
            location = entry.location.strip('][\' ')
            days = entry.days.strip('][\' ').replace('\'','')
            workout_type = entry.workout_type.strip('][\' ').replace('\'','')
            workout_type_set = set(workout_type.split(','))
            duration_set = set(duration.split(','))
            timezone_set = set(timezone.split(','))
            location_set = set(location.split(','))
            print(workout_type_filter_set)
            print(workout_type_set)
            print(location_filter_set)
            print(location_set)
            if(workout_type_filter_set.issubset(workout_type_set) & duration_filter_set.issubset(duration_set)\
            & time_zone_filter_set.issubset(timezone_set) & location_filter_set.issubset(location_set)):
                entry.workout_type = workout_type
                entry.days = days
                profiles.append(entry)
    workout_type_filter = str(workout_type_filter).strip('][\'')
    duration_filter = str(duration_filter).strip('][\'')
    time_zone_filter = str(time_zone_filter).strip('][\'')
    location_filter = str(location_filter).strip('][\'')
    return render(request,'buddyrequest/database.html',{'profiles':profiles,'time_zone_filter':\
    time_zone_filter,'workout_type_filter':workout_type_filter,'duration_filter':duration_filter,\
    'location_filter':location_filter})
@login_required(login_url='/accounts/login')
def remove_request(request):
    BuddyRequest.objects.get(user=request.user).delete()
    return redirect('home')
@login_required(login_url='/accounts/login')
def update_request(request):
    BuddyRequest.objects.get(user=request.user).delete()
    return redirect('find')
@login_required(login_url='/accounts/login')
def profile(request,request_id):
    # passed in user id as request_id when viewing user's own profile
    if(request.user.id == request_id):
        partner=BuddyRequest.objects.get(user = request.user)
    else:
        partner=BuddyRequest.objects.get(id = request_id)
    days=partner.days.strip('][\'').replace('\'','')
    workout_type=partner.workout_type.strip('][\'').replace('\'','')
    return render(request,'buddyrequest/profile.html',{'profile_details':partner,'days':days,'workout_type':workout_type})
@login_required(login_url='/accounts/login')
def partner_match(request,partner_id):
    if request.method=="POST":
        #partner object for current user
        user_request=BuddyRequest.objects.get(user=request.user)
        matched_user=User.objects.get(pk=partner_id)
        partner_request=BuddyRequest.objects.get(user=matched_user)
        # check if the partner already has a partner
        if(partner_request.partner != None):
            redirect('database')
        #match the two users in the database
        user_request.partner=matched_user
        partner_request.partner=request.user
        user_request.save()
        partner_request.save()

        #email both user and matched partner about the match
        mail(partner_request.name,user_request.netID,partner_request.netID,user=True,remove=False)
        mail(user_request.name,partner_request.netID,user_request.netID,user=False,remove=False)
        return redirect('partner')
@login_required(login_url='/accounts/login')
def matches(request):
    if request.method=='POST':
        #if the user already has a request or partner in the database, go back to home page
        requestsList=list(BuddyRequest.objects.all().values())
        netID = request.user.uniauth_profile.get_display_id()
        for entry in requestsList:
            if netID == entry['netID']:
                print("Problem here")
                print(entry)
                return redirect('home')
        print(netID)
        userdata = getStudentInfo(netID)
        preferences=request.POST.getlist('preferences')
        if(preferences == ['', '', '']):
            error = "Must rank preferences"
            return render(request, 'find.html',{'error': error})

        # reformatting preferences to match headers in matching algorithm
        preferences[preferences.index('Workout Days')] = 'days'
        preferences[preferences.index('Duration')] = 'duration'
        preferences[preferences.index('Time Zone')] = 'time_zone'

        print(preferences)
        error = ""
        try:
            name = userdata['full_name']
            major = userdata['major_raw']
            year = userdata['class_year']
            rescollege = userdata['res_college']
            days = request.POST.getlist('day')
            duration = int(request.POST['duration'])
            workout_type = request.POST.getlist('workout_type')
            time_zone = request.POST['time_zone']
            location = request.POST['location']
            intensity = request.POST['intensity']
            bio = request.POST['bio']

            if days == []:
                error = "Need to select at least one preferred day"
                raise Exception()
            if workout_type == []:
                error = "Need to select at least one preferred workout type"
                raise Exception()
        except Exception as e:
            print(e)
            if error == "": # will error if any of the fields are blank
                error = "Must fill out all fields in form"
            return render(request, 'find.html',{'error': error})

        user = request.user
        if(location == ''):
            location = 'EST'
        req_user=BuddyRequest(netID=netID,name=name,major=major,year=year,rescollege=rescollege,
        days=days,duration=duration,workout_type=workout_type,time_zone=time_zone,location=location,
        intensity=intensity,bio=bio,user=user)

        #data used for match
        user_data_list=[preferences,days,duration,workout_type,time_zone,intensity,location]

        req_user.save()

        #if there are no active requests, don't run matching algorithm
        if len(requestsList) < 1:
            return render(request,'buddyrequest/matches.html')
        else:
            matched_people = get_matches(user_data_list, requestsList)
            print(matched_people)
            if len(matched_people) > 3: # if more than 3 matches, give best 3
                return render(request,'buddyrequest/matches.html', {'matched_people':matched_people[0:2]})

            return render(request,'buddyrequest/matches.html',{'matched_people':matched_people})

@login_required(login_url='/accounts/login')
def partner(request):
    #Get the current user's partner by finding the user who's partner is the current user
    partner=BuddyRequest.objects.get(partner=request.user)
    days=partner.days.strip('][\'')
    workout_type=partner.workout_type.strip('][\'')
    return render(request,'buddyrequest/profile.html',{'profile_details':partner,'days':days,'workout_type':workout_type})

@login_required(login_url='/accounts/login')
def remove_partner(request):
    user = request.user
    user_request=BuddyRequest.objects.get(user = user)
    partner_request=BuddyRequest.objects.get(partner = user)
    mail(partner_request.name,user_request.netID,partner_request.netID,user=True,remove=True)
    mail(user_request.name,partner_request.netID,user_request.netID,user=False,remove=True)
    user_request.partner = None
    partner_request.partner = None
    user_request.save()
    partner_request.save()
    return redirect('home')
