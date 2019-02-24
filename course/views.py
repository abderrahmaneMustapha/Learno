from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from .models import( Subject, Course, Module, Content, ContentNote
,TakenCourse, TakenModule,TakenContent)
from .forms import ContentNoteForm
from accounts.models import Student




def subjects(request):
    subject = Subject.objects.all()
    return render(request,'course/subjects_form.html',{'subject' : subject})

@login_required
def courses(request, subject):
    subject_course = Course.objects.all()

    return render(request,'course/course_form.html',
    {'subject':subject ,'subject_course':subject_course, })
@login_required
def modules(request, subject, course):
    course_module = Module.objects.all()
    my_course= Course.objects.get(title=course)
    current_student =Student.objects.get(user=request.user)
    check_taken_course = TakenCourse.objects.filter(student = current_student, course=my_course)
    if check_taken_course.count()==0:
        new_taken_course = TakenCourse.objects.create(student = current_student, course=my_course)

    return render(request,'course/modules_form.html',
    {'course':course ,'course_module':course_module,})

@login_required
def contents(request, course, module):
    module_content= Content.objects.all()
    current_module= Module.objects.get(title=module)
    #current_student = Student.objects.get(user=request.user)
    check_taken_module = TakenModule.objects.filter(student = request.user.student, module=current_module )
    if check_taken_module.count() == 0:
        new_taken_module = TakenModule.objects.create(student=request.user.student, module=current_module)

    return render(request,'course/contents_form.html',
    {'module':module ,'module_content':module_content,})


@login_required
def learn(request, module, content):
    content_learn= Content.objects.get(title = content)
    current_student = Student.objects.get(user=request.user)
    check_taken_content = TakenContent.objects.filter(student = current_student, content=content_learn)
    if check_taken_content.count() ==0:
        new_taken_content =  TakenContent.objects.create(student = current_student, content=content_learn)
    note_form = ContentNoteForm()
    if request.method == "POST":
            note_form = ContentNoteForm(request.POST)
            if note_form.is_valid() :
                form = note_form.save(commit=False)
                form.user = request.user
                form.module = Module.objects.get(title = module)
                form.content = Content.objects.get(title=content)
                form.note = request.POST.get('note')
                form.save()

    return render(request,'course/learn_form.html',
    {'content':content ,'content_learn':content_learn, 'note_form' : note_form ,})
