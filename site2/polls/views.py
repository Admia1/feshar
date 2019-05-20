from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from .forms import RegisterForm, LoginForm
from django.contrib.auth import  login, logout
from .models import PollUser,Section
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
    template = 'polls/home2.html'

    if(request.user.is_authenticated):
        section_detail = [{day.shift : (day.related_users.count()<=3)} for day in Section.objects.order_by('-day')]
        return render(request, template, {'section_detail': section_detail, 'massage': massage})
    else:
        return HttpResponseRedirect(reverse('/register/'))

def take_view(request, section_pk):

    if(request.user.is_authenticated):
        section = Section.objects.get(pk=section_pk)
        if section.exists():
            if section.related_users.count()>=3:
                return HttpResponseRedirect(reverse('polls:home', args=("fulled section",)))
            else:
                section.related_users.get_or_create(pk = request.user.pk)
                return HttpResponseRedirect(revese('polls:home', args=("you reserved!",)))
        else:
            return HttpResponseRedirect(reverse('polls:home', args=("no such section",)))
    else:
        return HttpResponseRedirect(reverse('polls:register'))


def del_view(request, section_pk):
    if(request.user.is_authenticated):
        try:
            section = Section.objects.get(pk=section_pk)
            try:
                section.related_users.remove(pk=request.user.pk)
                return HttpResponseRedirect(revese('polls:home', args=('section removed')))
            except:
                return HttpResponseRedirect(revese('polls:home', args=('not reserved section')))
        except:
            return HttpResponseRedirect(reverse('polls:home', args=('no such section')))
    else:
        return HttpResponseRedirect(reverse('polls:register'))
