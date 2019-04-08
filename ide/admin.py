from django.contrib import admin
from .models import SupportedLanguages,Code,WebCode,OtherCode

admin.site.register(SupportedLanguages)
admin.site.register(Code)
admin.site.register(WebCode)
admin.site.register(OtherCode)
