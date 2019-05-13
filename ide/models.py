from django.db import models
from accounts.models import Student
from course.models import Course
from django.template.defaultfilters import slugify



class Code(models.Model):
    owner  = models.ForeignKey(Student, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=100, null=True)
    title = models.CharField(max_length= 50, null = True, unique=False)
    created = models.DateTimeField(auto_now_add = True)
    modified = models.DateTimeField(auto_now = True)
    def save(self, *args, **kwargs):
        self.slug= slugify(self.title)
        super(Code, self).save(*args, **kwargs)
    def __str__(self):
        return str(self.title)

class Vote(models.Model):
    owner = models.ForeignKey(Student, on_delete=models.CASCADE)
    code  = models.ForeignKey(Code, on_delete=models.CASCADE)

    class Meta:
         unique_together = ('code', 'owner')

    def __str__(self):
        return str(self.owner)



class SupportedLanguages(models.Model):
    name = models.TextField( max_length=500)
    created = models.DateField(auto_now_add=True)
    course = models.ForeignKey(Course,on_delete = models.CASCADE, null = True)



class OtherCode(models.Model):
    code = models.OneToOneField(Code, on_delete = models.CASCADE, unique = True)
    content =models.TextField( max_length=500)
    lang = models.ForeignKey(SupportedLanguages, on_delete = models.CASCADE)



class WebCode(models.Model):
    code = models.OneToOneField(Code, on_delete = models.CASCADE, unique=True)
    html = models.TextField( max_length=500)
    css = models.TextField( max_length=500)
    js = models.TextField( max_length=500)
