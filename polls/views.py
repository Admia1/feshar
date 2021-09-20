from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from .forms import RegisterForm, LoginForm, NationalIdForm, ExtraWorkForm, PaymentIdForm
from django.contrib.auth import  login, logout
from .models import PollUser,Section,USR,entry_year_show, ExtraWork
from django.urls import reverse

from redis import Redis
redis = Redis.from_url('redis://localhost:6379/1')
from pottery import Redlock
import jdatetime

def register_view(request):

    template = 'polls/register.html'
    if(request.user.is_authenticated):
        return HttpResponseRedirect(reverse('polls:home'))
    else:
        if request.method == 'POST':

            form = RegisterForm(request.POST)
            if form.is_valid():
                if User.objects.filter(username=form.cleaned_data['student_number']).exists():
                    return render(request, template, {
                        'form': form,
                        'error_message': 'شما قبلا ثبت نام کرده اید'
                    })
                else:
                    # Create the user:
                    user = User.objects.create_user(
                        username = form.cleaned_data['student_number'],
                        password = form.cleaned_data['phone_number'],
                    )
                    user.save()
                    polluser = PollUser(user = user)
                    polluser.first_name = form.cleaned_data['first_name']
                    polluser.last_name = form.cleaned_data['last_name']
                    polluser.phone_number = form.cleaned_data['phone_number']
                    polluser.national_id = form.cleaned_data['national_id']

                    polluser.entry_year = int(request.POST['entry_year'])
                    polluser.entry_year -= 1

                    polluser.student_number = form.cleaned_data['student_number']
                    polluser.can_presure = form.cleaned_data['can_presure']
                    polluser.sex = request.POST['sex']
                    polluser.save()

                    login(request, user)

                    return HttpResponseRedirect(reverse('polls:home'))
        else:
            form = RegisterForm()

        valid_entry = [entry_year_show(x) for x in range(14)]
        return render(request, template, {'form': form, 'valid_entry':valid_entry})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('polls:register'))


def login_view(request):
    template = 'polls/login.html'
    if request.user.is_authenticated :
        return HttpResponseRedirect(reverse('polls:home'))

    else:
        form = LoginForm(request.POST)

        if request.method == 'POST':
            if form.is_valid():
                if User.objects.filter(username=form.cleaned_data['username']).exists():
                    user = User.objects.get(username=form.cleaned_data['username'])
                    if user.check_password(form.cleaned_data['password']):
                        login(request, user)
                        return HttpResponseRedirect(reverse('polls:home'))

                return render(request, template, {
                    'form': form,
                    'error_message': 'شماره دانشجویی یا رمز عبور اشتباه می باشد'
                })

        else:
            form = LoginForm()
        return render(request, template, {'form': form})

def home_view(request):
    template = 'polls/home.html'
    if request.user.is_authenticated :
        polluser = PollUser.objects.get(user=request.user)
        if(polluser.national_id == "0"):#when user got no national_id
            return HttpResponseRedirect(reverse('polls:get_national_id'))
        if(not polluser.payment_id_valid()):
            return HttpResponseRedirect(reverse('polls:get_payment_id'))
        error_message = ""

        if request.method == 'POST':
            section = Section.objects.get(pk=request.POST['section_pk'])

            reserve_lock = Redlock(key=f"res_{section.pk}", masters={redis}, auto_release_time=60*1000)
            reserve_lock.acquire()

            usrs = section.usr_set.all()
            if len(usrs) >= 3:
                error_message = "این شیفت در این تاریخ و ایستگاه پر شده است"
            elif len(usrs)==2 and usrs[0].polluser.sex==usrs[1].polluser.sex==polluser.sex==0:
                error_message = "ا توجه به طرح تطبیق امکان حضور سه پسر در یک ایستگاه وجود ندارد!!!"
            else:
                # not supported for current jdatetime
                #if USR.objects.filter(section__end__mt=section.start, section__start__lt=section.end, polluser=polluser).exists():
                if [usr for usr in USR.objects.filter(polluser=polluser) if (usr.section.start<section.end and usr.section.end>section.start)]:
                    error_message = "شما قبلا در این روز و تاریخ شیفتی رزرو کرده اید"
                else:
                    #todo
                    if section.available_from <= jdatetime.datetime.now():
                        USR.objects.create(polluser=polluser, section=section)
                        error_message = "رزرو شد"
                    else:
                        error_message = "هم اکنون امکان رزرو شیفت وجود ندارد"

            reserve_lock.release()
        #  day.section_set.order_by('index', 'station')
        sections = [section for section in Section.objects.filter(available_from__lt=jdatetime.datetime.now()) if section.usr_set.count()<3]

        user_usr = [usr for usr in USR.objects.filter(polluser__user=request.user).order_by('section__start')]
        return render(request, template, {'sections': sections, 'error_message': error_message, 'user_usr': user_usr, 'polluser':polluser})
    else:
        return HttpResponseRedirect(reverse('polls:register'))

def delete_view(request, usr_pk):
    if request.user.is_authenticated :
        try:
            usr = USR.objects.get(pk=usr_pk)
            try:
                if usr.polluser.user == request.user:
                    if usr.section.deletable_until > jdatetime.datetime.now():
                        usr.delete()
                return HttpResponseRedirect(reverse('polls:home'))
            except:
                return HttpResponseRedirect(reverse('polls:home'))
        except:
            return HttpResponseRedirect('polls:home')
    else:
        return HttpResponseRedirect(reverse('polls:register'))


def sections_view(request):
    if request.user.is_staff or request.user.is_superuser:
        template = 'polls/sections.html'
        error_message=""
        needed_dates=[  ('start','زمان شروع'),
                        ('end','زمان پایان'),
                        ('available_from','قابل رزرو از'),
                        ('deletable_until','قابل لغو تا')]
        if request.method == 'POST':
            dates=dict()
            header = request.POST.get('header')
            detail = request.POST.get('detail')

            if not header:
                error_message = "عنوان خالی است"
            elif not detail:
                error_message = "جزییات خالی است"
            else:
                try:
                    for t,name in needed_dates:
                        dates[t] = jdatetime.datetime(
                                        int(request.POST.get(f"{t}__year")),
                                        int(request.POST.get(f"{t}__month")),
                                        int(request.POST.get(f"{t}__day")),
                                        int(request.POST.get(f"{t}__hour")),
                                        int(request.POST.get(f"{t}__minute")),)
                except:
                    error_message= "ورودی نامناسب"
                # available < deletable <= start < end
                if not error_message:
                    if dates['available_from'] >= dates['deletable_until']:
                        error_message= "آخربن زمان مجاز حذف باید پس از زمان مجاز ثبت رزور باشد"
                    elif dates['deletable_until'] > dates['start']:
                        error_message= "زمان قابل رزرو شدن باید پس قبل از زمان شروع باشد"
                    elif dates['start'] >= dates['end']:
                        error_message= "زمان پایان باید پس از زمان شروع باشد"
                    else:
                        Section.objects.create(header=header, detail=detail,
                            start=dates['start'], end=dates['end'],
                            available_from=dates['available_from'],
                            deletable_until=dates['deletable_until'])

        ### cubing by date
        dic={}
        dates=[]
        for section in Section.objects.all():
            date = section.start.date()
            if date not in dic:
                dates.append(date)
                dic[date] = [section]
            if date in dic:
                dic[date].append(section)

        sections = [dic[date] for date in dates]
        ###  end of cubing by date
        current_datetime = jdatetime.datetime.now()
        months= ['فروردین','اردیبهشت','خرداد','تیر','مرداد','شهریور','مهر','آبان','آذر','دی','بهمن','اسفند']
        return render(request, template, {'sections':sections, 'months':months, 'current_datetime':current_datetime, 'needed_dates':needed_dates, 'error_message':error_message})
    else:
        return HttpResponseRedirect(reverse('polls:home'))

def user_view(request ,polluser_pk):
    if request.user.is_staff or request.user.is_superuser:
        template = 'polls/user.html'
        try:
            polluser = PollUser.objects.get(pk = polluser_pk)
            if request.method == 'POST':
                form = ExtraWorkForm(request.POST)
                if form.is_valid():
                    ew = ExtraWork(polluser=polluser, hour=form.cleaned_data['hour'] ,info=form.cleaned_data['info'])
                    ew.save()
                    return HttpResponseRedirect(reverse('polls:user',  kwargs={'polluser_pk' : polluser.pk}))
            form = ExtraWorkForm()
            return render(request, template, {'polluser' : polluser, 'form' : form})
        except:
            return render(request, template, {'error_message': "همچین کاربری وجود ندارد"})
    else:
        return HttpResponseRedirect(reverse('polls:home'))

def users_view(request):
    if request.user.is_staff or request.user.is_superuser:
        template = 'polls/users.html'
        pollusers = PollUser.objects.order_by('entry_year')
        return render(request, template, {'pollusers':pollusers})
    else:
        return HttpResponseRedirect(reverse('polls:home'))

def gp_student_view(request):
    if request.user.is_staff or request.user.is_superuser:
        template = 'polls/gpstudent.html'
        pollusers = PollUser.objects.order_by('entry_year')
        return render(request, template, {'pollusers':pollusers})
    else:
        return HttpResponseRedirect(reverse('polls:home'))

def ngp_student_view(request):
    if request.user.is_staff or request.user.is_superuser:
        template = 'polls/ngpstudent.html'
        pollusers = PollUser.objects.order_by('entry_year')
        return render(request, template, {'pollusers':pollusers})
    else:
        return HttpResponseRedirect(reverse('polls:home'))

def cant_view(request):
    if request.user.is_staff or request.user.is_superuser:
        template = 'polls/cant.html'
        pollusers = PollUser.objects.order_by('entry_year')
        return render(request, template, {'pollusers':pollusers})
    else:
        return HttpResponseRedirect(reverse('polls:home'))




def get_national_id_view(request):
    # if this is a POST request we need to process the form data
    template = 'polls/get_national_id.html'
    if(request.user.is_authenticated):
        if request.method == 'POST':
            form = NationalIdForm(request.POST)
            if form.is_valid():
                polluser = PollUser.objects.get(user=request.user)
                polluser.national_id = form.cleaned_data['national_id']
                polluser.save()
                return HttpResponseRedirect(reverse('polls:home'))
        else:
            form = NationalIdForm()
        return render(request, template, {'form': form})
    return HttpResponseRedirect(reverse('polls:register'))

def get_payment_id_view(request):
    # if this is a POST request we need to process the form data
    template = 'polls/get_payment_id.html'
    if(request.user.is_authenticated):
        error_message = ""
        if request.method == 'POST':
            form = PaymentIdForm(request.POST)
            if form.is_valid():
                payment_id = form.cleaned_data['payment_id']
                #if len(payment_id) == 16:
                if 1==1:
                    polluser = PollUser.objects.get(user=request.user)
                    polluser.payment_id = payment_id
                    polluser.save()
                    return HttpResponseRedirect(reverse('polls:home'))
                else:
                    error_message = "طول شماره حساب باید 16 رفم باشد!!!"
                    form = PaymentIdForm()
                    return render(request, template, {'form': form, 'error_message': error_message})
        else:
            form = PaymentIdForm()
        return render(request, template, {'form': form})
    return HttpResponseRedirect(reverse('polls:register'))


def table_user_view(request):
    if request.user.is_staff or request.user.is_superuser:
        template = 'polls/table_user.html'
        pollusers = PollUser.objects.order_by('entry_year')
        return render(request, template, {'pollusers':pollusers})
    else:
        return HttpResponseRedirect(reverse('polls:home'))

def table_shift_view(request):
    if request.user.is_staff or request.user.is_superuser:
        template = 'polls/table_shift.html'
        ### cubing by date
        dic={}
        dates=[]
        for section in Section.objects.all():
            date = section.start.date()
            if date not in dic:
                dates.append(date)
                dic[date] = [section]
            if date in dic:
                dic[date].append(section)

        sections = [dic[date] for date in dates]
        ###  end of cubing by date
        return render(request, template, {'sections' : sections})
    else:
        return HttpResponseRedirect(reverse('polls:home'))


def section_view(request ,section_pk):
    if request.user.is_staff or request.user.is_superuser:
        template = 'polls/section.html'
        try:
            section = Section.objects.get(pk=section_pk)
            usrs = USR.objects.filter(section=section)
            return render(request, template, {'section' : section, 'usrs' : usrs})
        except:
            return render(request, template, {'error_message': "همچین شیفتی وجود ندارد"})
    else:
        return HttpResponseRedirect(reverse('polls:home'))

def change_present_view(request, usr_pk, new_state):
    if request.user.is_staff or request.user.is_superuser:
        try:
            usr = USR.objects.get(pk=usr_pk)
            usr.is_present = new_state
            usr.save()
            return HttpResponseRedirect(reverse('polls:section', kwargs={'section_pk' : usr.section.pk}))
        except:
            raise
            template = 'polls/section.html'
            return render(request, template, {'error_message': "همچین"})
    else:
        return HttpResponseRedirect(reverse('polls:home'))

def delete_extra_work(request, extra_work_pk, polluser_pk):
    if request.user.is_staff or request.user.is_superuser:
        try :
            extra_work = ExtraWork.objects.get(pk = extra_work_pk)
            extra_work.delete()
            return HttpResponseRedirect(reverse('polls:user' ,kwargs={'polluser_pk' : polluser_pk}))
        except:
            return HttpResponseRedirect(reverse('polls:user' ,kwargs={'polluser_pk' : polluser_pk}))
    return HttpResponseRedirect(reverse('polls:home'))

def staff_veiw(request, polluser_pk, new_state):
    if request.user.is_superuser:
        try:
            user = PollUser.objects.get(pk=polluser_pk).user
            user.is_staff = new_state
            user.save()
            HttpResponseRedirect(reverse('polls:user' ,kwargs={'polluser_pk' : polluser_pk}))
        except:
            HttpResponseRedirect(reverse('polls:user' ,kwargs={'polluser_pk' : polluser_pk}))
    return HttpResponseRedirect(reverse('polls:home'))
