from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from .forms import RegisterForm, LoginForm, NationalIdForm
from django.contrib.auth import  login, logout
from .models import PollUser,Section,EventDay,USR,entry_year_show
from django.urls import reverse

def register_view(request):
    # if this is a POST request we need to process the form data
    template = 'polls/register.html'
    if(request.user.is_authenticated):
        return HttpResponseRedirect(reverse('polls:home'))
    else:
        if request.method == 'POST':
            # create a form instance and populate it with data from the request:
            form = RegisterForm(request.POST)
            # check whether it's valid:
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
                    # polluser.entry_year = form.cleaned_data['entry_year']
                    polluser.national_id = form.cleaned_data['national_id']
                    polluser.entry_year = int(request.POST['entry_year'])
                    polluser.entry_year -= 1
                    polluser.student_number = form.cleaned_data['student_number']
                    polluser.can_presure = form.cleaned_data['can_presure']
                    polluser.sex = request.POST['sex']
                    polluser.save()


                    login(request, user)

                    # redirect to accounts page:
                    return HttpResponseRedirect(reverse('polls:home'))

       # No post data availabe, let's just show the page.
        else:
            form = RegisterForm()

        valid_entry = [entry_year_show(x) for x in range(14)]
        return render(request, template, {'form': form, 'valid_entry':valid_entry})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('polls:register'))


def login_view(request):
    # if this is a POST request we need to process the form data
    template = 'polls/login.html'

    if request.user.is_authenticated :
        return HttpResponseRedirect(reverse('polls:home'))

    else:
        form = LoginForm(request.POST)

        if request.method == 'POST':
            # check whether it's valid:
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

       # No post data availabe, let's just show the page.
        else:
            form = LoginForm()
        return render(request, template, {'form': form})

def home_view(request):
    template = 'polls/home.html'
    if request.user.is_authenticated :
        polluser = PollUser.objects.get(user=request.user)
        if(polluser.national_id == "0"):#when user got no national_id
            return HttpResponseRedirect(reverse('polls:get_national_id'))
        error_message = ""

        if request.method == 'POST':
            section = Section.objects.get(pk=request.POST['section_pk'])

            usrs = section.usr_set.all()
            if len(usrs) >= 3:
                error_message = "این شیفت در این تاریخ و ایستگاه پر شده است"
            elif len(usrs)==2 and usrs[0].polluser.sex==usrs[1].polluser.sex==polluser.sex:
                error_message = "با توجه به طرح تطبیق امکان حضور سه پسر یا سه دختر در یک ایستگاه وجود ندارد!!!"
            else:
                if USR.objects.filter(section__eventday=section.eventday, section__index=section.index, polluser=polluser).exists():
                    error_message = "شما قبلا در این روز و تاریخ شیفتی رزرو کرده اید"
                else:
                    USR.objects.create(polluser=polluser, section=section)
                    error_message = "رزرو شد"

        section_detail = [[section for section in day.section_set.order_by('index', 'station') if section.usr_set.count()<3] for day in EventDay.objects.all().order_by('day')]
        usr_detail = [usr for usr in USR.objects.filter(polluser__user=request.user)]
        return render(request, template, {'section_detail': section_detail, 'error_message': error_message, 'usr_detail': usr_detail})
    else:
        return HttpResponseRedirect(reverse('polls:register'))



def delete_view(request, usr_pk):
    if request.user.is_authenticated :
        try:
            usr = USR.objects.get(pk=usr_pk)
            try:
                if usr.polluser.user == request.user:
                    usr.delete()
                return HttpResponseRedirect(reverse('polls:home'))
            except:
                return HttpResponseRedirect(reverse('polls:home'))
        except:
            return HttpResponseRedirect('polls:home')

    else:
        return HttpResponseRedirect(reverse('polls:register'))


def info_view(request):
    if request.user.is_staff:
        template = 'polls/info.html'
        section_detail = [[section for section in day.section_set.order_by('index', 'station')] for day in EventDay.objects.all().order_by('day')]
        return render(request, template, {'section_detail' : section_detail})
    else:
        return HttpResponseRedirect(reverse('polls:home'))

def info_user_view(request ,polluser_pk):
    if request.user.is_staff:
        template = 'polls/userinfo.html'
        try:
            polluser = PollUser.objects.get(pk = polluser_pk)
            return render(request, template, {'polluser' : polluser})
        except:
            return render(request, template, {'error_message': "همچین کاربری وجود ندارد"})
    else:
        return HttpResponseRedirect(reverse('polls:home'))

def allusers_view(request):
    if request.user.is_staff:
        template = 'polls/allusers.html'
        pollusers = PollUser.objects.order_by('entry_year')
        return render(request, template, {'pollusers':pollusers})
    else:
        return HttpResponseRedirect(reverse('polls:home'))

def gp_student_view(request):
    if request.user.is_staff:
        template = 'polls/gpstudent.html'
        pollusers = PollUser.objects.order_by('entry_year')
        return render(request, template, {'pollusers':pollusers})
    else:
        return HttpResponseRedirect(reverse('polls:home'))

def ngp_student_view(request):
    if request.user.is_staff:
        template = 'polls/ngpstudent.html'
        pollusers = PollUser.objects.order_by('entry_year')
        return render(request, template, {'pollusers':pollusers})
    else:
        return HttpResponseRedirect(reverse('polls:home'))

def cant_view(request):
    if request.user.is_staff:
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


def table_user_view(request):
    if request.user.is_staff:
        template = 'polls/table_user.html'
        pollusers = PollUser.objects.order_by('entry_year')
        return render(request, template, {'pollusers':pollusers})
    else:
        return HttpResponseRedirect(reverse('polls:home'))

def table_shift_view(request):
    if request.user.is_staff:
        template = 'polls/table_shift.html'
        section_detail = [[section for section in day.section_set.order_by('index', 'station')] for day in EventDay.objects.all().order_by('day')]
        return render(request, template, {'section_detail' : section_detail})
    else:
        return HttpResponseRedirect(reverse('polls:home'))


def section_view(request ,section_pk):
    if request.user.is_staff:
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
    if request.user.is_staff:
        try:
            usr = USR.objects.get(pk=usr_pk)
            usr.is_present = new_state
            usr.save()
            return HttpResponseRedirect(reverse('polls:section', 'section_pk'=usr.section.pk))
        except:
            raise
            template = 'polls/section.html'
            return render(request, template, {'error_message': "همچین"})
    else:
        return HttpResponseRedirect(reverse('polls:home'))
