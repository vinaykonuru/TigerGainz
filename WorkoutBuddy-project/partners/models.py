from django.db import models
from django.contrib.auth.models import User
from buddyrequest.models import BuddyRequest

# Create your models here.
class Partners(models.Model):
    netID=models.CharField(max_length=50)
    name=models.CharField(max_length=50)
    major=models.CharField(max_length=50)
    year=models.CharField(max_length=50)
    rescollege=models.CharField(max_length=50)
    profile_picture=models.ImageField(upload_to='images/',default='default_profile_picture.png')
    days=models.CharField(max_length=300)
    duration=models.CharField(max_length=50)
    workout_type=models.CharField(max_length=50)
    time_zone=models.CharField(max_length=50)
    group_size=models.IntegerField(default=2)
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="user")
    partner=models.ForeignKey(User,on_delete=models.CASCADE,related_name="partner")
