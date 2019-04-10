from django.urls import path
from django.conf.urls.static import static
from . import views
from  django.conf import settings

from rest_framework import routers



urlpatterns = [

      path('', views.ide_index, name='coding-ground'),
      path('<str:language>/', views.main_editor, name="main-editor"),
      path('shared-frontend/<slug>/<pk>/', views.share_frontend, name='share-editor-frontend'),
      path('shared-code/<slug>/<pk>/', views.share_code, name='share-editor-code'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
