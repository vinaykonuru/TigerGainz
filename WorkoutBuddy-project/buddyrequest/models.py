from django.db import models
from django.contrib.auth.models import User
import json
# Create your models here.
class BuddyRequest(models.Model):
    netID=models.CharField(max_length=50)
    name=models.CharField(max_length=50)
    major=models.CharField(max_length=50)
    year=models.CharField(max_length=50)
    rescollege=models.CharField(max_length=50)
    days=models.CharField(max_length=300)
    duration=models.CharField(max_length=50)
    workout_type=models.CharField(max_length=50)
    time_zone=models.CharField(max_length=50)
    group_size=models.IntegerField(default=2)
    user=models.ForeignKey(User,on_delete=models.CASCADE)

    def set_days(self,x):
        self.days=json.dumps(x)
    def get_days(self):
        return json.loads(self.days)
