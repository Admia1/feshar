from django.db import models
from django.contrib.auth.models import User

def sex_show(x):
    if(x==0):
        return "آقای"
    if(x==1):
        return "خانم"
    return "جنسیت"

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
    sex = models.IntegerField(default=1)

    def show_year(self):
        return entry_year_show(self.entry_year)

    def show_name(self):
        return sex_show(self.sex) + " " + self.first_name + " " + self.last_name

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
    station = models.IntegerField(default=1)

    def show(self):

        if self.station ==1 :
            ret = "ایسنگاه اول "
        if self.station ==2 :
            ret = "ایستگاه دوم "
        if self.station ==3 :
            ret = "ایستگاه سوم"

        if(self.index==1):
            ret+=  " شیفت اول ساعت ۸ الی ۱۱"
        if(self.index==2):
            ret+= " شیفت دوم ساعت ۱۱ الی ۱۴"
        if(self.index==3):
            ret+= " شیفت سوم ساعت ۱۴ الی ۱۷"
        if(self.index==4):
            ret+= " شیفت چهارم ساعت ۱۷ الی ۲۰"
        ret = self.eventday.show() + ret
        return ret

    def is_full(self):
        return self.usr_set.count() >= 3

    def anti_tatbiq(self):
        if self.usr_set.count() == 3:
            a=0
            for usr in self.usr_set.all():
                a+=usr.polluser.sex

            if a==0 :
                return True
            elif a==3 :
                if self.station == 3:
                    return True
        elif self.usr_set.count() >  3:
            return True
        return False

    def show_detail(self):
        ret = self.show()
        if self.usr_set.count() >= 3:
            ret += " پر است!! "
        return ret

class USR(models.Model):
    polluser = models.ForeignKey(PollUser ,on_delete=models.CASCADE)
    section = models.ForeignKey(Section ,on_delete=models.CASCADE)
