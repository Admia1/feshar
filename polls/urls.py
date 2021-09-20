from django.conf.urls import url
from . import views
from django.urls import path

app_name = 'polls' # So we can use it like: {% url 'mymodule:user_register' %} on our template.
urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout.', views.logout_view, name='logout'),
    path('home/', views.home_view, name='home'),
    path('users/', views.users_view, name='users'),
    path('ngp/', views.ngp_student_view, name='ngp'),
    path('gp/', views.gp_student_view, name='gp'),
    path('cant/', views.cant_view, name='cant'),
    path('get_national_id/', views.get_national_id_view, name='get_national_id'),
    path('get_payment_id/', views.get_payment_id_view, name='get_payment_id'),
    path('table_shift/', views.table_shift_view, name='table_shift'),
    path('table_user/', views.table_user_view , name='table_user'),


    #url('take/', views.take_view ,name='take'),
    path('delete/<int:usr_pk>/', views.delete_view ,name='delete'),
    path('user/<int:polluser_pk>/', views.user_view, name='user'),
    path('section/<int:section_pk>/', views.section_view, name='section'),

    path('change_usr_present/<int:usr_pk>/<int:new_state>/', views.change_present_view, name='change_usr_present'),
    path('sections/', views.sections_view, name='sections'),

    path('delete_extra_work/<int:extra_work_pk>/<int:polluser_pk>/', views.delete_extra_work ,name='delete_extra_work'),

    path('staff/<int:polluser_pk>/<int:new_state>', views.staff_veiw, name='staff_state'),

    path('', views.register_view, name='base'),
]
