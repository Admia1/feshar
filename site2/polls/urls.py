from django.conf.urls import url
from . import views

app_name = 'polls' # So we can use it like: {% url 'mymodule:user_register' %} on our template.
urlpatterns = [
    url('login', views.user_login, name='login'),
    url('logout', views.user_logout, name='logout'),
    url('', views.user_register, name='register'),
]
