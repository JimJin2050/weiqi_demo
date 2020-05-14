# -*- coding=utf-8 -*-
import socket
import json
from datetime import datetime
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.template.loader import get_template
from django import forms
from .models import Teachers, Students, Classes
from rest_framework import viewsets
from django.core import serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework import request
from rest_framework import permissions
from rest_framework.response import Response
from .forms import *
from .utils import *

# name = socket.getfqdn(socket.gethostname())
# name = name.strip(".localdomain") if name.endswith(".localdomain") else name
# myaddr = socket.gethostbyname(name)
# myport = "8888"
# now = datetime.now()

def teacher_login(request):
    if request.method == 'POST':
        loginform = TeacherLoginForm(request.POST)
        if loginform.is_valid():
            username = loginform.cleaned_data['username']
            password = loginform.cleaned_data['password']
            user = Teachers.objects.filter(username__exact=username, password__exact=password)
            if user:
                request.session['is_login'] = '1'
                request.session['user_id'] = user[0].username
                return redirect('/teacher/')
            else:
                return HttpResponse('用户名或密码错误,请重新登录')
    else:
        loginform = TeacherLoginForm()
    return render(
        request,
        'teacher_login.html',
        {
            'loginform': loginform,
            'now': datetime.now()
        })


def student_login(request):
    if request.method == 'POST':
        loginform = StudentLoginForm(request.POST)
        if loginform.is_valid():
            username = loginform.cleaned_data['username']
            password = loginform.cleaned_data['password']
            user = Students.objects.filter(username__exact=username, password__exact=password)
            print(user)
            if user:
                request.session['is_login'] = '1'
                request.session['student_id'] = user[0].username
                return redirect('/student/')
            else:
                return HttpResponse('用户名或密码错误,请重新登录')
    else:
        loginform = StudentLoginForm()
    return render(
        request,
        'student_login.html',
        {
            'loginform': loginform,
            'now': datetime.now()
        })


def teacher_register(request):
    if request.method == 'POST':
        teacherform = TeacherForm(request.POST)
        if teacherform.is_valid():
            username = teacherform.cleaned_data['username']
            password = teacherform.cleaned_data['password']
            email = teacherform.cleaned_data['email']

            user = Teachers.objects.create(username=username, password=password, email=email)
            user.save()
            #return HttpResponse('register success!!!')
            return redirect('/teacher/login')
    else:
        teacherform = TeacherForm()

    return render(
        request,
        'teacher_register.html',
        {
            'userform': teacherform,
            'now': datetime.now()
        })


def student_register(request):
    if request.method == 'POST':
        studentform = StudentForm(request.POST)
        if studentform.is_valid():
            username = studentform.cleaned_data['username']
            name = studentform.cleaned_data['name']
            password = studentform.cleaned_data['password']
            level = studentform.cleaned_data['level']
            class_id = studentform.cleaned_data['class_id']
            email = studentform.cleaned_data['email']

            user = Students.objects.create(
                username=username,
                name=name,
                password=password,
                level=level,
                class_id=class_id,
                email=email)
            user.save()
            return redirect('/student/login/')
    else:
        studentform = StudentForm()

    return render(
        request,
        'student_register.html',
        {
            'userform': studentform,
            'now': datetime.now()
        })


def show_student(request, idx):
    template = get_template('student_detail.html')
    try:
        student = Students.objects.get(sid=idx)
        if student:
            locals().update({'now': datetime.now()})
            html = template.render(locals())
            return HttpResponse(html)
    except Exception as e:
        print(e)
        return redirect('/teacher/')


def add_class(request):
    if request.method == 'POST':
        classform = ClassForm(request.POST)
        if classform.is_valid():
            classname = classform.cleaned_data['classname']
            owner = classform.cleaned_data['owner']
            myclass = Classes.objects.create(
                classname=classname, 
                owner=Teachers.objects.get(username=owner))
            myclass.save()
            #return HttpResponse('register success!!!')
            return redirect('/teacher/')
    else:
        classform = ClassForm()

    return render(
        request,
        'add_class.html',
        {
            'classform': classform,
            'now': datetime.now()
        })


def play(request):
    pass


def get_student(request):
    user_id = request.session.get('student_id')
    userobj = Students.objects.filter(username=user_id)
    user = userobj[0] if userobj else None
    print(userobj, user)

    page = request.GET.get('page')
    if page:
        page = int(page)
    else:
        page = 1
    print('PAGE 参数为：', page)
    student_list = Students.objects.filter(username=user_id).order_by("sid")

    paginator = Paginator(student_list, 200)
    page_job_list = paginator.page(page)
    page_num = paginator.num_pages

    # print('page_num:',page_num);
    if page_job_list.has_next():
        next_page = page + 1
    else:
        next_page = page

    if page_job_list.has_previous():
        previous_page = page - 1
    else:
        previous_page = page

    return render(request, 'student_index.html', {
        'student_list': page_job_list,
        'page_num': range(1, page_num + 1),
        'curr_page': page,
        'next_page': next_page,
        'previous_page': previous_page,
        'user': user,
        'now': datetime.now(),
        'addr': get_ip(),
        'port': get_port(),
        'cur_port': request.META['SERVER_PORT'],
    })


def get_students(request):
    user_id = request.session.get('user_id')
    userobj = Teachers.objects.filter(username=user_id)
    user = userobj[0] if userobj else None

    page = request.GET.get('page')
    if page:
        page = int(page)
    else:
        page = 1
    myclasses = Classes.objects.filter(owner=user)
    student_list = Students.objects.filter(class_id__in=myclasses).order_by("sid")

    paginator = Paginator(student_list, 200)
    page_job_list = paginator.page(page)
    page_num = paginator.num_pages

    # print('page_num:',page_num);
    if page_job_list.has_next():
        next_page = page + 1
    else:
        next_page = page

    if page_job_list.has_previous():
        previous_page = page - 1
    else:
        previous_page = page

    return render(request, 'teacher_index.html', {
        'student_list': page_job_list,
        'page_num': range(1, page_num + 1),
        'curr_page': page,
        'next_page': next_page,
        'previous_page': previous_page,
        'user': user,
        'now': datetime.now()
    })


@api_view(http_method_names=['GET'])
@permission_classes((permissions.AllowAny,))
def all_students(request):
    students = serializers.serialize("json", Students.objects.all())
    data = {
        'students': students
    }
    return Response(data)


@api_view(http_method_names=['POST'])
@permission_classes((permissions.AllowAny,))
def save_result(request):
    data = json.loads(request.body)
    winner, player1, player2 = data["winner"], data["player_black"], data["player_white"]
    player1_obj = Students.objects.filter(username=player1)[0]
    player2_obj = Students.objects.filter(username=player2)[0]
    if player1 == winner:
        calculate_and_update(player1_obj, player2_obj)
    else:
        calculate_and_update(player2_obj, player1_obj)
    data = {
        'success': 1
    }
    return Response(data)


def calculate_and_update(player1_obj, player2_obj):
    level_dict = {
        '15K': 1,
        '14K': 2,
        '13K': 3,
        '12K': 4,
        '11K': 5,
        '10K': 6,
        '9K': 7,
        '8K': 8,
        '7K': 9,
        '6K': 10,
        '5K': 11,
        '4K': 12,
        '3K': 13,
        '2K': 14,
        '1K': 15,
        '1D': 16,
        '2D': 17,
        '3D': 18,
        '4D': 19,
        '5D': 20,
        '6D': 21,
        '7D': 22,
        '8D': 23
    }
    lvl_dict = {v: k for k, v in level_dict.items()}
    level1 = player1_obj.level
    level2 = player1_obj.level
    player1_obj.winning_streak += 1
    player1_obj.losing_streak = 0
    player1_obj.num_of_win += 1
    player2_obj.losing_streak += 1
    player2_obj.winning_streak = 0
    player2_obj.num_of_failure += 1

    if level1 == level2:
        player1_obj.credits += 2
        player2_obj.credits -= 2
    elif level_dict[level1] < level_dict[level2]:
        increment = abs(level_dict[level1] - level_dict[level2]) * 3
        player1_obj.credits += increment
        player2_obj.credits -= increment
    else:
        player1_obj.credits += 1
        player1_obj.credits -= 1

    if player1_obj.winning_streak >= 10:
        lvl = level_dict[level1] + 1
        lvl = 23 if lvl > 23 else lvl
        player1_obj.level = lvl_dict[lvl]
        player1_obj.winning_streak = 0

    if player2_obj.losing_streak >= 5:
        lvl = level_dict[level1] - 1
        lvl = 1 if lvl < 1 else lvl
        player2_obj.level = lvl_dict[lvl]
        player2_obj.losing_streak = 0
    player1_obj.save()
    player2_obj.save()
