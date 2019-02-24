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

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
