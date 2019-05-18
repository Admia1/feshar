from django.db import models
from django.contrib.auth.models import User

class Puser(models.Model):
    user = models.OneToOneField(User ,on_delete=models.CASCADE)
    can_presure = models.BooleanField(default=0)
    more_detail_1 = models.CharField(max_length=200, default="")
    more_detail_2 = models.CharField(max_length=200, default="")

class Section(models.Model):
    work_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    related_users = models.ManyToManyField(Puser)
