from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import pandas
def home(request):
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

        #put into csv
        f = open("user.csv", "w")
        headers='Name,Day_Av,Duration,Type_Workout,Time_z,No_Ppl \n'
        data=''+name+','+days+','+duration+','+workout_type+','+time_zone+','+group_size+'\n'
        f.write(headers)
        f.write(data)
        #formula
        #do something in the requests list
        return redirect('waiting')
    else:
        return render(request,'home.html')

@login_required(login_url='/accounts/signup')
def find(request):
    return render(request,'find.html')

@login_required(login_url='/accounts/signup')
def waiting(request):
    return render(request,'waiting.html')

@login_required(login_url='/accounts/signup')
def about(request):
    return render(request,'about.html')
