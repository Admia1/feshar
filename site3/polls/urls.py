from django.conf.urls import url
from . import views
from django.urls import path

app_name = 'polls' # So we can use it like: {% url 'mymodule:user_register' %} on our template.
urlpatterns = [
    url('register/', views.register_view, name='register'),
    url('login/', views.login_view, name='login'),
    url('logout.', views.logout_view, name='logout'),
    url('home/', views.home_view, name='home'),
    url('users/', views.users_view, name='users'),
    url('ngp/', views.ngp_student_view, name='ngp'),
    url('gp/', views.gp_student_view, name='gp'),
    url('cant/', views.cant_view, name='cant'),
    url('get_national_id/', views.get_national_id_view, name='get_national_id'),
    url('table_shift/', views.table_shift_view, name='table_shift'),
    url('table_user/', views.table_user_view , name='table_user'),


    #url('take/', views.take_view ,name='take'),
    path('delete/<int:usr_pk>/', views.delete_view ,name='delete'),
    path('user/<int:polluser_pk>/', views.user_view, name='user'),
    path('section/<int:section_pk>/', views.section_view, name='section'),

    path('chang_usr_present/<int:usr_pk>/<int:new_state>/', views.change_present_view, name='chang_usr_present'),
    url('sections/', views.sections_view, name='sections'),
    url('', views.register_view, name='base'),
]
