from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from .forms import RegisterForm, LoginForm
from django.contrib.auth import  login, logout
from .models import PollUser,Section,EventDay,USR
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
                        'error_message': 'student number already exists.'
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
                    polluser.entry_year = form.cleaned_data['entry_year']
                    polluser.student_number = form.cleaned_data['student_number']
                    polluser.can_presure = form.cleaned_data['can_presure']
                    polluser.save()


                    login(request, user)

                    # redirect to accounts page:
                    return HttpResponseRedirect(reverse('polls:home'))

       # No post data availabe, let's just show the page.
        else:
            form = RegisterForm()

        return render(request, template, {'form': form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('polls:register'))


def login_view(request):
    # if this is a POST request we need to process the form data
    template = 'polls/login.html'

    if(request.user.is_authenticated):
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
                    'error_message': 'Wrong username or password'
                })

       # No post data availabe, let's just show the page.
        else:
            form = LoginForm()
        return render(request, template, {'form': form})


def home_view(request, massage = ""):
    # if this is a POST request we need to process the form data
    template = 'polls/home.html'

    if(request.user.is_authenticated):
        section_detail = [[section for section in day.section_set.order_by('index')] for day in EventDay.objects.all().order_by('-day')]
        usr_detail = [usr for usr in USR.objects.filter(user=request.user)]
        return render(request, template, {'section_detail': section_detail, 'massage': massage, 'usr_detail': usr_detail})
    else:
        return HttpResponseRedirect(reverse('polls:register'))

def take_view(request):
    if(request.user.is_authenticated):
        section = Section.objects.get(pk=request.POST['section_pk'])
        if section:
            if section.usr_set.count()>=3:
                return HttpResponseRedirect(reverse('polls:home'))
            else:
                USR.objects.get_or_create(user = request.user, section=section)
                return HttpResponseRedirect(reverse('polls:home'))
        else:
            return HttpResponseRedirect(reverse('polls:home'))
    else:
        return HttpResponseRedirect(reverse('polls:register'))


def delete_view(request, usr_pk):
    if(request.user.is_authenticated):
        try:
            usr = USR.objects.get(pk=usr_pk)
            try:
                if usr.user == request.user:
                    usr.delete()
                return HttpResponseRedirect(reverse('polls:home'))
            except:
                return HttpResponseRedirect(reverse('polls:home'))
        except:
            return HttpResponseRedirect('polls:register')

    else:
        return HttpResponseRedirect(reverse('polls:register'))
