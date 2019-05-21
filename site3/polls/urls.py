from django.conf.urls import url
from . import views
from django.urls import path

app_name = 'polls' # So we can use it like: {% url 'mymodule:user_register' %} on our template.
urlpatterns = [
    url('register/', views.register_view, name='register'),
    url('login/', views.login_view, name='login'),
    url('logout.', views.logout_view, name='logout'),
    url('home/', views.home_view, name='home'),
    url('take/', views.take_view ,name='take'),
    path('delete/<int:usr_pk>/', views.delete_view ,name='delete'),
    path('info/<int:polluser_pk>/', views.info_user_view, name='userinfo'),
     url('info/', views.info_view, name='info'),
    url('', views.register_view, name='base'),
]
