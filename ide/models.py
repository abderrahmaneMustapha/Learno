from django.db import models
from accounts.models import Student


class Code(models.Model):
    owner  = models.ForeignKey(Student, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add = True)
    modified = models.DateTimeField(auto_now = True)

class Vote(models.Model):
    up  = 0
    down = 1

    STATUS_CHOICES =  ( (up, "up"), (down, "down"), )
    owner = models.ForeignKey(Student, on_delete=models.CASCADE)
    code  = models.ForeignKey(Code, on_delete=models.CASCADE)
    vote = models.IntegerField(choices = STATUS_CHOICES, null = True)

    def __str__(self):
        return self.owner

class SupportedLanguages(models.Model):
    name = models.TextField( max_length=500)
    created = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.name


class OtherCode(models.Model):
    code = models.OneToOneField(Code, on_delete = models.CASCADE)
    content =models.TextField( max_length=500)
    lang = models.ForeignKey(SupportedLanguages, on_delete = models.CASCADE)


class WebCode(models.Model):
    code = models.OneToOneField(Code, on_delete = models.CASCADE)
    css = models.TextField( max_length=500)
    js = models.TextField( max_length=500)
    html = models.TextField( max_length=500)
