from django import forms
from .models import Subject,Course,Module,ContentNote, Content, TakenCourse
from accounts.models import Tag
class CourseForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
       queryset=Tag.objects.all(),
       widget=forms.CheckboxSelectMultiple,
       required=False
   )

    class Meta:
        model = Course
        fields = ('title', 'tags', 'overview')
        widgets = {'tags' : forms.CheckboxSelectMultiple ,
                  }



class ContentNoteForm(forms.ModelForm):

    class Meta:
        model = ContentNote
        fields = ('user','content','note')
        widgets = {'user': forms.HiddenInput(),
                    'content': forms.HiddenInput()}
