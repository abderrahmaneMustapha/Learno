from django import forms
from .models import Subject,Course,Module,ContentNote, Content, TakenCourse

class SubjectForm(forms.ModelForm):

    class Meta:
        model = Subject
        fields = ('title','description','photo')


class ContentNoteForm(forms.ModelForm):

    class Meta:
        model = ContentNote
        fields = ('user','content','note')
        widgets = {'user': forms.HiddenInput(),
                    'content': forms.HiddenInput()}
