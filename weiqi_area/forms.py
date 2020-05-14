# -*- coding=utf-8 -*-
from django import forms
from .models import Teachers, Students, Classes


class TeacherForm(forms.Form):
    username = forms.CharField(label='用户', max_length=50)
    password = forms.CharField(label='密码', widget=forms.PasswordInput())
    email = forms.EmailField(label='邮箱')


class TeacherLoginForm(forms.Form):
    username = forms.CharField(label='用户', max_length=50)
    password = forms.CharField(label='密码', widget=forms.PasswordInput())


class StudentForm(forms.Form):
    username = forms.CharField(label='用户', max_length=50)
    password = forms.CharField(label='密码', widget=forms.PasswordInput())
    name = forms.CharField(label='姓名', max_length=50)
    class_id = forms.ModelChoiceField(
        queryset=Classes.objects.all(),
        label='班级',
        empty_label='请选择要加入的班级')
    email = forms.EmailField(label='邮箱')
    level = forms.ChoiceField(
        initial=1,
        choices=(
            ('15K', '15K'), ('14K', '14K'), ('13K', '13K'), ('12K', '12K'),
            ('11K', '11K'), ('10K', '10K'), ('9K', '9K'), ('8K', '8K'), ('7K', '7K'),
            ('6K', '6K'), ('5K', '5K'), ('4K', '4K'), ('3K', '3K'), ('2K', '2K'),
            ('1K', '1K'), ('1D', '1D'), ('2D', '2D'), ('3D', '3D'), ('4D', '4D'),
            ('5D', '5D'), ('6D', '6D'), ('7D', '7D'), ('8D', '8D')),
        label='段位'
    )


class StudentLoginForm(forms.Form):
    username = forms.CharField(label='用户', max_length=50)
    password = forms.CharField(label='密码', widget=forms.PasswordInput())


class ClassForm(forms.Form):
    classname = forms.CharField(label='班级', max_length=30)
    owner = forms.ModelChoiceField(
        queryset=Teachers.objects.all(),
        label='老师',
        empty_label='请您选择新班级老师')
