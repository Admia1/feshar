from django.db import models
from django.contrib.auth.models import User

def entry_year_show(x):
    arr = [
    "مهر ۹۷",
    "بهمن ۹۷",
    "مهر ۹۶",
    "بهمن ۹۶",
    "مهر ۹۵",
    "بهمن ۹۵",
    "مهر ۹۴",
    "بهمن ۹۴",
    "مهر ۹۳",
    "بهمن ۹۳",
    "مهر ۹۲",
    "بهمن ۹۲",
    "مهر ۹۱",
    "بهمن ۹۱",
    ]
    if(x<len(arr)):
        return arr[x];
    else:
        return "سالی که وارد شد"
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

    def show_year(self):
        return entry_year_show(self.entry_year)

    def show_name(self):
        return self.first_name + " " + self.last_name

    def can_str(self):
        if self.can_presure:
            return "بله"
        else:
            return "خیر"
    def __str__(self):
        return self.first_name + " " + self.last_name
    def f_student_number(self):
        return farsi(self.student_number)
    def f_phone_number(self):
        return farsi(self.phone_number)


class EventDay(models.Model):
    day = models.IntegerField()

    def show(self):
        if self.day<100:
           return farsi(self.day)+" خرداد "
        else:
            return farsi(self.day-100)+" تیر "

class Section(models.Model):
    eventday = models.ForeignKey(EventDay, on_delete=models.CASCADE)
    index = models.IntegerField(default=1)
    def show(self):
        if(self.index==1):
            ret=  " شیفت اول ساعت ۸ الی ۱۰:۳۰"
        if(self.index==2):
            ret= " شیفت دوم ساعت ۱۰:۳۰ الی ۱۳"
        if(self.index==3):
            ret= " شیفت سوم ساعت ۱۶ الی ۱۸:۳۰"
        if(self.index==4):
            ret= " شیفت چهارم ساعت ۱۸:۳۰ الی ۲۱"
        ret = self.eventday.show() + ret
        return ret

    def show_detail(self):
        ret = self.show()
        if self.usr_set.count() >= 3:
            ret += " پر است!! "
        return ret

class USR(models.Model):
    polluser = models.ForeignKey(PollUser ,on_delete=models.CASCADE)
    section = models.ForeignKey(Section ,on_delete=models.CASCADE)
