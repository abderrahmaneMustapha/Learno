from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.utils import timezone


from accounts.models import Student, Tag, Badge, Question


from tinymce.models import HTMLField
from colorful.fields import RGBColorField

class Subject (models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, null=True, blank=True)
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to='subject_photos/', blank=True,)
    approved = models.BooleanField(default=False)
    color = RGBColorField(max_length=7, default='#007bff')
    verified = models.BooleanField(default=False)
    def save(self, *args, **kwargs):
        self.slug= slugify(self.title)
        super(Subject, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.title)

class Course(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='created_course')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE,related_name='courses')
    title = models.CharField(max_length=200)
    tags = models.ManyToManyField(Tag, blank =True, default =None, related_name='tag_courses' )
    overview = models.TextField()
    created = models.DateField(auto_now_add=True)
    photo = models.ImageField(upload_to='courses_photos/', blank=True,)
    approved = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    slug = models.SlugField(max_length=200, null=True, blank=True)
    def save(self, *args, **kwargs):
        self.slug= slugify(self.title)
        super(Course, self).save(*args, **kwargs)
    class Meta:
        ordering =['-created']
    def __str__(self):
        return  str(self.title)
    def get_course_tags(self):
        return str(list(self.tags.all().values_list('name', flat=True)))


class Module(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE, related_name='course_modules')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(unique=True)
    photo = models.ImageField(upload_to='modules_photos/', blank=True,)
    approved = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    slug = models.SlugField(max_length=200, null=True, blank=True)
    def save(self, *args, **kwargs):
        self.slug= slugify(self.title)
        super(Module, self).save(*args, **kwargs)
    class Meta:
        ordering = ['order']

    def __str__(self):
        return '{}. {}'.format(self.order, self.title)

class Content(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE,related_query_name='module_contents')
    title = models.CharField(max_length=200, blank=True)
    question = models.OneToOneField(Question, on_delete=models.CASCADE, related_query_name='question_contents', null=True, blank=True)
    text = HTMLField()
    video = models.URLField(blank=True)
    image = models.ImageField(upload_to='content/image/',blank=True)
    order = models.PositiveIntegerField(unique=True)
    approved = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    slug = models.SlugField(max_length=200, null=True, blank=True)
    def save(self, *args, **kwargs):
        self.slug= slugify(self.title)
        super(Content, self).save(*args, **kwargs)
    class Meta:
        ordering = ['order']

    def __str__(self):
        return '{}. {}'.format(self.order, self.title)


class ContentNote(models.Model):
    user = models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE, related_name='created_note')
    content = models.ForeignKey(Content,blank=True,null=True, on_delete=models.CASCADE,related_query_name='content_note')
    note = models.TextField(max_length=300)

    def __str__(self):
        return '{} {} '.format(self.user , self.content)


class TakenCourse(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE, related_name='student_course' )
    subject  = models.ForeignKey(Subject,on_delete=models.CASCADE,default = None, related_name='course_subject_taken')
    course  = models.ForeignKey(Course,on_delete=models.CASCADE, related_name='course_taken')
    date = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField (default=False)

    def __str__(self):
        return str(self.course.title)

class TakenModule(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE, related_name='student_module' )
    course  = models.ForeignKey(Course,on_delete=models.CASCADE, default=None, related_name='module_course_taken')
    module =  models.ForeignKey(Module,on_delete=models.CASCADE, related_name='module_taken')
    date = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    def __str__(self):
        return str(self.module.title)

class TakenContent(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE, related_name='student_content' )
    module =  models.ForeignKey(Module,on_delete=models.CASCADE, default=None, related_name='content_module_taken')
    content = models.ForeignKey(Content,on_delete=models.CASCADE, related_name='content_taken')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.content.title)
