from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Group(models.Model):
    studentOne=models.ForeignKey(User,on_delete=models.CASCADE)
    studentTwo=models.ForeignKey(User,on_delete=models.CASCADE)
