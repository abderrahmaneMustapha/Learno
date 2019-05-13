from rest_framework import serializers
from .models import Student

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('pk' , 'photo', 'interests', 'exp', 'rank', 'level')
        #read_only_fields  = fields
