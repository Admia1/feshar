from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .forms import RegisterForm, LoginForm
from django.contrib.auth import  login,logout
from .models import Puser

def user_register(request):
    # if this is a POST request we need to process the form data
    template_register = 'polls/register.html'
    template_loged_in = 'polls/logedin.html'
    if(request.user.is_authenticated):
        return render(request, template_loged_in )
    else:
        if request.method == 'POST':
            # create a form instance and populate it with data from the request:
            form = RegisterForm(request.POST)
            # check whether it's valid:
            if form.is_valid():
                if User.objects.filter(username=form.cleaned_data['username']).exists():
                    return render(request, template_register, {
                        'form': form,
                        'error_message': 'Username already exists.'
                    })
                elif User.objects.filter(email=form.cleaned_data['email']).exists():
                    return render(request, template_register, {
                        'form': form,
                        'error_message': 'Email already exists.'
                    })
                elif form.cleaned_data['password'] != form.cleaned_data['password_repeat']:
                    return render(request, template_register, {
                        'form': form,
                        'error_message': 'Passwords do not match.'
                    })
                else:
                    # Create the user:
                    user = User.objects.create_user(
                        form.cleaned_data['username'],
                        form.cleaned_data['email'],
                        form.cleaned_data['password']
                    )
                    user.first_name = form.cleaned_data['first_name']
                    user.last_name = form.cleaned_data['last_name']
                    orm.cleaned_data['last_name']
                    user.phone_number = form.cleaned_data['phone_number']
                    user.save()

                    puser = Puser(
                        user=user
                    )
                    puser.save()

                    # Login the user
                    login(request, user)

                    # redirect to accounts page:
                    return HttpResponseRedirect('/')

       # No post data availabe, let's just show the page.
        else:
            form = RegisterForm()

        return render(request, template_register, {'form': form})


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


def user_login(request):
    # if this is a POST request we need to process the form data
    template_login    = 'polls/login.html'
    template_loged_in = 'polls/logedin.html'

    if(request.user.is_authenticated):
        return render(request, template_loged_in)


    else:
        if request.method == 'POST':
            # create a form instance and populate it with data from the request:
            form = LoginForm(request.POST)
            # check whether it's valid:
            if form.is_valid():
                if User.objects.filter(username=form.cleaned_data['username']).exists():
                    user = User.objects.get(username=form.cleaned_data['username'])
                    if user.check_password(form.cleaned_data['password']):
                        login(request, user)
                        return HttpResponseRedirect('/')

                return render(request, template_login, {
                    'form': form,
                    'error_message': 'Wrong username or password'
                })

       # No post data availabe, let's just show the page.
        else:
            form = LoginForm()
        return render(request, template_login, {'form': form})
