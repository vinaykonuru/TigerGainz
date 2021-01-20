from django.db import models
from django.contrib.auth.models import User
import json
# Create your models here.
class BuddyRequest(models.Model):
    netID=models.CharField(max_length=50,null=True)
    name=models.CharField(max_length=50, null=True)
    major=models.CharField(max_length=50, null=True)
    year=models.CharField(max_length=50, null=True)
    rescollege=models.CharField(max_length=50,null=True)
    days=models.CharField(max_length=300,null=True)
    duration=models.IntegerField(null=True)
    workout_type=models.CharField(max_length=50,null=True)
    time_zone=models.CharField(max_length=50,null=True)
    location=models.CharField(max_length=50,null=True)
    intensity=models.CharField(max_length=50,null=True)
    bio=models.TextField(default='',null=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE, related_name='user',null=True)
    partner=models.ForeignKey(User,on_delete=models.CASCADE,related_name='partner',null=True,blank=True)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)

    def set_days(self,x):
        self.days=json.dumps(x)
    def get_days(self):
        return json.loads(self.days)
