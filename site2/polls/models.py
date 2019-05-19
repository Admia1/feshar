from django.db import models
from django.contrib.auth.models import User

class PollUser(models.Model):
    user = models.ForeignKey(User ,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, default="FIRST_NAME")
    last_name = models.CharField(max_length=100, default="LAST_NAME")
    phone_number  = models.CharField(max_length=20, default="0917")
    student_number = models.CharField(max_length=20, default="1234")
    entry_year = models.IntegerField()

    can_presure = models.BooleanField(default=0)



class Section(models.Model):
    work_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    related_users = models.ManyToManyField(PollUser)
