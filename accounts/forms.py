from django import forms
from django.contrib.auth.models import User

from .models import Student,Tag,Quiz, Answer, Question




class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.CharField(required=True)
    class Meta:
         model = User
         fields = ("username", "password",'email',)


class StudentForm(forms.ModelForm):
     photo = forms.ImageField(required=False)
     interests = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
     class Meta:
         model = Student
         fields = ('photo','interests',)
         widgets = {'interests': forms.CheckboxSelectMultiple}

class EditUserForm(forms.ModelForm):
    class Meta:
         model = User
         fields = ("username", "password",'email',)


class AnswerForm(forms.Form):
    text = forms.CharField(required = True, max_length=100)
    class Meta:
        fields = ('text')
