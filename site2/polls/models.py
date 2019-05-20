from django.db import models
from django.contrib.auth.models import User

def farsi(x):
    x=str(x)
    num = {
    '0':'۰',
    '1':'۱',
    '2':'۲',
    '3':'۳',
    '4':'۴',
    '5':'۵',
    '6':'۶',
    '7':'۷',
    '8':'۸',
    '9':'۹',
    }
    for y in num:
        x=x.replace(y,num[y])
    return x



class PollUser(models.Model):
    user = models.ForeignKey(User ,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, default="FIRST_NAME")
    last_name = models.CharField(max_length=100, default="LAST_NAME")
    phone_number  = models.CharField(max_length=20, default="0917")
    student_number = models.CharField(max_length=20, default="1234")
    entry_year = models.IntegerField()

    can_presure = models.BooleanField(default=0)

class EventDay(models.Model):
    day = models.IntegerField()

    def show(self):
        return farsi(self.day)+" خرداد "

class Section(models.Model):
    eventday = models.ForeignKey(EventDay, on_delete=models.CASCADE)
    index = models.IntegerField(default=1)
    def show(self):
        if(self.index==1):
            ret=  " شیفت اول "
        if(self.index==2):
            ret= " شیفت دوم "
        if(self.index==3):
            ret= " شیفت سوم "
        if(self.index==4):
            ret= " شیفت چهارم "
            
        ret+= self.eventday.show()

        if self.usr_set.count() >= 3:
            ret += " پر است!! "

        return ret

class USR(models.Model):
    user = models.ForeignKey(User ,on_delete=models.CASCADE)
    section = models.ForeignKey(Section ,on_delete=models.CASCADE)
