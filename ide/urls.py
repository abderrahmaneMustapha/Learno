from django.urls import path
from django.conf.urls.static import static
from . import views
from  django.conf import settings

from rest_framework import routers

app_name = 'ide'
urlpatterns = [

    path('', views.ide_index, name='index'),
    path('compile/', views.compile_code, name='compile'),
    path('run/', views.run_code, name='run'),
    path('<code_id>/', views.saved_code_view, name='saved-code'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
