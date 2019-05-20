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

class EventDay(models.Model):
    day = models.DateField()
    

class Section(models.Model):
    eventday = models.ForeignKey(EventDay, on_delete=models.CASCADE)
    index = models.IntegerField(default=1)
    def show(self):
        return "Time #%d"%self.index

class USR(models.Model):
    user = models.ForeignKey(User ,on_delete=models.CASCADE)
    section = models.ForeignKey(Section ,on_delete=models.CASCADE)
