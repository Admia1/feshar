from django.conf.urls import url
from . import views

app_name = 'polls' # So we can use it like: {% url 'mymodule:user_register' %} on our template.
urlpatterns = [
    url('take/<int:section_pk>/', views.take_view ,name='take'),
    url('delete/<int:section_pk>/', views.delete_view ,name='delete'),
    url('home', views.home_view, name='home'),
    url('login', views.login_view, name='login'),
    url('logout', views.logout_view, name='logout'),
    url('', views.register_view, name='register'),
]
