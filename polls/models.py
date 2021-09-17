from django.db import models
from django.contrib.auth.models import User
from django_jalali.db import models as jmodels

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
def farsi(number):
    number_string = str(number)
    farsi_dictionary = {
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
    for digit in number_string:
        number_string = number_string.replace(digit, farsi_dictionary[digit])
    return number_string



class PollUser(models.Model):
    user = models.ForeignKey(User ,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, default="FIRST_NAME")
    last_name = models.CharField(max_length=100, default="LAST_NAME")
    national_id = models.CharField(max_length=20,default="0")
    student_number = models.CharField(max_length=20, default="1234")
    phone_number  = models.CharField(max_length=20, default="0917")
    entry_year = models.IntegerField()
    can_presure = models.BooleanField(default=0)
    sex = models.IntegerField(default=1)
    payment_id = models.CharField(max_length=100, default="0000000000000000")

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

    def f_national_id(self):
        return farsi(self.national_id)

    def is_gp_student(self):
        if len(self.student_number) == 10:
            if self.student_number[2:7] == "12104":
                return True
        return False

    def f_usr_count(self):
        return farsi(self.usr_set.count())

    def present_time(self):
        return 3 * self.usr_set.filter(is_present = True).count()

    def extra_time(self):
        time = 0
        for extra_work in self.extrawork_set.all():
            time += extra_work.hour
        return time

    def reserved_time(self):
        return 3 * self.usr_set.count()

    def total_time(self):
        return self.present_time() + self.extra_time()

    def f_present_time(self):
        return farsi(self.present_time())

    def f_total_time(self):
        return farsi(self.total_time())

    def f_reserved_time(self):
        return farsi(self.reserved_time())

    def payment_id_valid(self):
        return self.payment_id != "0000000000000000"

    def payment_id_show(self):
        output_string = self.payment_id[0:4] + "_" + self.payment_id[5:8] + "_" +self.payment_id[9:12] + "_" +self.payment_id[13:16]
        return output_string

class EventDay(models.Model):
    day = models.IntegerField()

    def show(self):
        if self.day<31:
           return farsi(self.day)+" خرداد "
        else:
            return farsi(self.day-31)+" تیر "

    def __str__(self):
        return self.show()

class Section(models.Model):
    eventday = models.ForeignKey(EventDay, on_delete=models.CASCADE)
    index = models.IntegerField(default=1)
    station = models.IntegerField(default=1)
    start = jmodels.jDateTimeField()
    end = jmodels.jDateTimeField()


    def detail_show(self):
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

        return ret


    def show(self):
        return self.eventday.show() + self.detail_show()

    def __str__(self):
        return self.show()

    def is_full(self):
        return self.usr_set.count() >= 3

    def anti_tatbiq(self):
        number_of_girls =0
        for usr in self.usr_set.all():
            number_of_girls += usr.polluser.sex
        if number_of_girls==0 :
            return True

    def show_detail(self):
        output = self.show()
        if self.usr_set.count() >= 3:
            output += " پر است!! "
        return output

class USR(models.Model):
    polluser = models.ForeignKey(PollUser ,on_delete=models.CASCADE)
    section = models.ForeignKey(Section ,on_delete=models.CASCADE)
    is_present = models.BooleanField(default = False)

    def ip_show(self):
        if self.is_present:
            return "حاضر"
        else:
            return "غائب"

    def ip_color(self):
        if self.is_present:
            return 'green'
        else:
            return 'red'


class Config(models.Model):
    first_deleteable_day = models.IntegerField(default=0)
    site_online = models.IntegerField(default=0 )

class ExtraWork(models.Model):
    polluser = models.ForeignKey(PollUser, on_delete=models.CASCADE)
    info = models.CharField(default="اضافه کاری", max_length = 100)
    hour = models.IntegerField(default=0)

    def f_hour(self):
        return farsi(self.hour)
