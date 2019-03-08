from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from colorful.fields import RGBColorField
from accounts.models import Student, Tag, Badge

class Subject (models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to='subject_photos/', blank=True,)
    approved = models.BooleanField(default=False)
    color = RGBColorField(max_length=7, default='#007bff')
    verified = models.BooleanField(default=False)


    def __str__(self):
        return self.title

class Course(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='created_course')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE,related_name='courses')
    title = models.CharField(max_length=200)
    tags = models.ManyToManyField(Tag, blank =True, default =None, related_name='tag_courses' )
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(upload_to='courses_photos/', blank=True,)
    approved = models.BooleanField(default=False)

    verified = models.BooleanField(default=False)

    class Meta:
        ordering =['-created']
    def __str__(self):
        return  self.title


class Module(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE, related_name='course_modules')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    source = models.URLField(default = None, blank =True)
    order = models.PositiveIntegerField(unique=True)
    photo = models.ImageField(upload_to='modules_photos/', blank=True,)
    approved = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return '{}. {}'.format(self.order, self.title)

class Content(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE,related_query_name='module_contents')
    title = models.CharField(max_length=200, blank=True)
    text = models.TextField()
    video = models.URLField(blank=True)
    file = models.FileField(upload_to='content/file/',blank=True)
    image = models.ImageField(upload_to='content/image/',blank=True)
    order = models.PositiveIntegerField(unique=True)
    approved = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return '{}. {}'.format(self.order, self.title)


class ContentNote(models.Model):
    user = models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE, related_name='created_note')
    content = models.ForeignKey(Content,blank=True,null=True, on_delete=models.CASCADE,related_query_name='content_note')
    note = models.TextField(max_length=300)

    def __str__(self):
        return '{}  {} {} '.format(self.user, self.module , self.content)


class TakenCourse(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE, related_name='student_course' )
    subject  = models.ForeignKey(Subject,on_delete=models.CASCADE,default = None, related_name='course_subject_taken')
    course  = models.ForeignKey(Course,on_delete=models.CASCADE, related_name='course_taken')
    date = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(null=True)
    def __str__(self):
        return str(self.course.title)

class TakenModule(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE, related_name='student_module' )
    course  = models.ForeignKey(Course,on_delete=models.CASCADE, default=None, related_name='module_course_taken')
    module =  models.ForeignKey(Module,on_delete=models.CASCADE, related_name='module_taken')
    date = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(null=True)
    def __str__(self):
        return str(self.module.title)

class TakenContent(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE, related_name='student_content' )
    module =  models.ForeignKey(Module,on_delete=models.CASCADE, default=None, related_name='content_module_taken')
    content = models.ForeignKey(Content,on_delete=models.CASCADE, related_name='content_taken')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.content.title)
