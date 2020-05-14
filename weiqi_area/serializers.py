from .models import Students
from rest_framework import serializers


class StudentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Students
        fields = ('username', 'name', 'level', 'class_id', 'credits')
