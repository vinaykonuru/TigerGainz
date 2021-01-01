from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

import csv

def home(request):
    user = request.user
    print(user.uniauth_profile.get_display_id())
    return render(request,'home.html')

def about(request):
    return render(request,'about.html')

def contacts(request):
    return render(request,'contact.html')

@login_required(login_url='/accounts/signup')
def find(request):
    return render(request,'find.html')


def excercise_guide(request):
    return render(request,'excercise_guide.html')
