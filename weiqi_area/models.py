from __future__ import unicode_literals

from django.db import models


class Teachers(models.Model):
    username = models.CharField(max_length=50, primary_key=True)
    password = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):
        return self.username


class Classes(models.Model):
    cid = models.BigAutoField(primary_key=True)
    classname = models.CharField(max_length=30, unique=True)
    owner = models.ForeignKey('Teachers', on_delete=models.CASCADE)

    def __str__(self):
        return self.classname


class Students(models.Model):
    sid = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=50)
    name = models.CharField(max_length=50, default="")
    password = models.CharField(max_length=50)
    level = models.CharField(max_length=5)
    class_id = models.ForeignKey('Classes', on_delete=models.CASCADE)
    credits = models.BigIntegerField(default=0)
    num_of_win = models.BigIntegerField(default=0)
    num_of_failure = models.BigIntegerField(default=0)
    winning_streak = models.BigIntegerField(default=0)
    losing_streak = models.BigIntegerField(default=0)
    email = models.EmailField()

    def __str__(self):
        return self.username


class Logs(models.Model):
    login_datetime = models.DateTimeField()
    student = models.ForeignKey('Students', on_delete=models.CASCADE)


class PlayRecords(models.Model):
    pid = models.BigAutoField(primary_key=True)
    play_datetime = models.DateTimeField()
    student_a = models.ForeignKey(
        'Students',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='甲',
        related_name='student_a')
    student_b = models.ForeignKey(
        'Students',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='乙',
        related_name='student_b')
    result = models.CharField(max_length=200)
