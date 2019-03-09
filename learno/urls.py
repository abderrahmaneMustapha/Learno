
from django.contrib import admin
from django.urls import path, include
from . import settings
from django.conf.urls.static import static

admin.site.index_template = 'my_custom_index.html/'
admin.autodiscover()
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('course/', include('course.urls')),
    path('api-auth/' ,include('rest_framework.urls'))

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
