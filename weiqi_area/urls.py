from django.urls import path, re_path, include
from django.conf.urls import url
# from rest_framework import routers
from . import views

urlpatterns = [
    path('teacher/login/', views.teacher_login, name='login'),
    path('teacher/register/', views.teacher_register, name='teacher_register'),
    re_path(r'^student/(\w+)$', views.show_student, name='student_detail'),
    path('teacher/newclass/', views.add_class, name='add_class'),
    path('teacher/', views.get_students, name='teacher_index'),
    path('student/register/', views.student_register, name='student_register'),
    path('student/login/', views.student_login, name='student_login'),
    path('student/', views.get_student, name='student_index'),
    url(r'^users/get/$', views.all_students),
    url(r'^result/save/$', views.save_result),
]
