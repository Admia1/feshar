from django.conf.urls import url
from . import views
from django.urls import path

app_name = 'polls' # So we can use it like: {% url 'mymodule:user_register' %} on our template.
urlpatterns = [
    url('register/', views.register_view, name='register'),
    url('take/', views.take_view ,name='take'),
    path('delete/<int:usr_pk>/', views.delete_view ,name='delete'),
    url('home/', views.home_view, name='home'),
    url('login/', views.login_view, name='login'),
    url('logout.', views.logout_view, name='logout'),
    url('', views.register_view, name='base'),
]
