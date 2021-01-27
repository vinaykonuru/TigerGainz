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
            print(entry.duration)
            duration = str(entry.duration).strip('][\'').replace(' \'','\'')
            timezone = entry.time_zone.strip('][\' ')
            location = entry.location.strip('][\' ')
            days = entry.days.strip('][\' ').replace('\'','')
            workout_type = entry.workout_type.replace(' ','').strip('][\'').replace('\'','')
            workout_type_set = set(workout_type.split(','))
            duration_set = set(duration.split(','))
            timezone_set = set(timezone.split(','))
            location_set = set(location.split(','))
            print("sets")
            print(workout_type_set)
            print(duration_set)
            print(timezone_set)
            print(location_set)
            print('filters')
            print(workout_type_filter_set)
            print(duration_filter_set)
            print(time_zone_filter_set)
            print(location_filter_set)
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
    partner.days=partner.days.strip('][\'').replace('\'','')
    partner.workout_type=partner.workout_type.strip('][\'').replace('\'','')
    return render(request,'buddyrequest/profile.html',{'profile_details':partner})
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
        print(requestsList)
        print(type(requestsList[0]))
        for entry in requestsList:
            print(entry['partner_id'])
            print(type(entry['partner_id']))

            if entry['partner_id'] != None:
                print('in if statement')
                requestsList.remove(entry)
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
        # getting index
        time_zone_rank = preferences.index('Time Zone')
        workoutDays_rank = preferences.index('Workout Days')
        duration_rank = preferences.index('Duration')

        # assigning index to proper place in preferences list
        preferences[0] = time_zone_rank
        preferences[1] = workoutDays_rank
        preferences[2] = duration_rank

        print(preferences)
        error = ""
        try:
            name = userdata['full_name']
            major = userdata['major_raw']
            year = userdata['class_year']
            rescollege = userdata['res_college']
            days = request.POST.getlist('day')
            duration = int(request.POST['duration'])
            workout_type = str(request.POST.getlist('workout_type'))
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
            for entry in matched_people: # remove all requests that already have partners and fix reformatting
                entry[6] = entry[6].strip('][\'').replace('\'','')
                entry[8] = entry[8].strip('][\'').replace('\'','')
                print(entry[14])
                print(type(entry[14]))
                if type(entry[14]) == "<class 'int'>":
                    matched_people.remove(entry)
            if len(matched_people) > 3: # if more than 3 matches, give best 3
                return render(request,'buddyrequest/matches.html', {'matched_people':matched_people[0:3]})
            return render(request,'buddyrequest/matches.html',{'matched_people':matched_people})

@login_required(login_url='/accounts/login')
def partner(request):
    #Get the current user's partner by finding the user who's partner is the current user
    partner=BuddyRequest.objects.get(partner=request.user)
    partner.days=partner.days.strip('][\'').replace('\'','')
    partner.workout_type=partner.workout_type.strip('][\'').replace('\'','')
    return render(request,'buddyrequest/profile.html',{'profile_details':partner})

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
