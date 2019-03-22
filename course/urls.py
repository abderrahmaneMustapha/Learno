from django.urls import path, include

from django.conf.urls.static import static
from . import views
from  django.conf import settings

urlpatterns = [
    path('subjects/', views.subjects, name = 'subjects'),

    path('subjects/<subject>/', views.courses, name = 'courses'),


    path('subjects/<subject>/courses/<course>/', views.modules, name = 'modules'),

    path('courses/<course>/modules/<module>/', views.contents, name = 'contents'),

    path('modules/<module>/content/<content>/', views.learn, name = 'learn'),
    path('modules/<module>/content/<content>/<question>/', views.learn_question, name = 'learn-question'),


    #add course
    path('subjects/<subject>/courses/add', views.add_course, name = 'add-course'),

    #add module
    path('courses/<course>/modules/add', views.add_module, name = 'add-module'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
