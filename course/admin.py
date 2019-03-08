from django.contrib import admin
from .models import (Content, Course, Subject, Module,ContentNote,
 TakenCourse, TakenModule, TakenContent)

class ContentAdmin(admin.ModelAdmin):
    list_display = ['title', 'module']
    list_filter = ('module','title')

class ModuleAdmin(admin.ModelAdmin):
    list_display = ['title', 'course','approved']
    list_filter = ('title','course','approved')

class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'owner','created',]
    list_filter = ('subject','title')

class ContentNoteAdmin(admin.ModelAdmin):
    list_display = ['user', 'content']
    list_filter = ('user','content')

class TakenCourseAdmin(admin.ModelAdmin):
    list_display = ['student', 'course','date']
    list_filter = ('student','course')

class TakenModuleAdmin(admin.ModelAdmin):
    list_display = ['student', 'module','date']
    list_filter = ('student','module')

class TakenContentAdmin(admin.ModelAdmin):
    list_display = ['student', 'module','content','date']
    list_filter = ('student','module','content','date')


admin.site.register(Subject)

admin.site.register(Content, ContentAdmin)
admin.site.register(Module, ModuleAdmin)
admin.site.register(Course, CourseAdmin)

#track user
admin.site.register(ContentNote, ContentNoteAdmin)
admin.site.register(TakenCourse, TakenCourseAdmin)
admin.site.register(TakenModule, TakenModuleAdmin)
admin.site.register(TakenContent, TakenContentAdmin)
