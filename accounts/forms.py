from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import *
from .models import Student,Tag,Quiz, Answer, Question
from django.utils import timezone



class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    password_confirmation = forms.CharField(widget=forms.PasswordInput(),
     label = 'Password Confirmation', required = True)
    email = forms.CharField(required=True)
    class Meta:
         model = User
         fields = ("username", "password", "password_confirmation" ,'email',)
    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        password_confirmation = cleaned_data.get("password_confirmation")
        user = super(UserForm, self)
        if password != password_confirmation or validate_password(password, user=user) is not None:
            raise forms.ValidationError(
                "password and password confirmation does not match",
                password_validators_help_texts(),

            )
    def save(self, commit=True):
        user = super(UserForm, self).save(commit)
        user.last_login = timezone.now()
        if commit:
            user.save()
        return user

class StudentForm(forms.ModelForm):
     photo = forms.ImageField(required=False)
     interests = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
     class Meta:
         model = Student
         fields = ('bio','photo','interests',)
         widgets = {'interests': forms.CheckboxSelectMultiple}

class EditUserForm(forms.ModelForm):
    class Meta:
         model = User
         fields = ('username','email',)


class SearchForm(forms.Form):
    search = forms.CharField(max_length= 25)

class ContactUs(forms.Form):
    name = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=100)
    subject= forms.CharField(max_length=100)
    text = forms.CharField(max_length=500, widget =forms.Textarea)
