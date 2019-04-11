from django.contrib import admin
from .models import SupportedLanguages,Code,WebCode,OtherCode

class SupportedLanguagesAdmin(admin.ModelAdmin):
    list_display = ['name', 'created']
    list_filter = ('created',)


class CodeAdmin(admin.ModelAdmin):
    list_display = ['owner', 'title', 'created', 'modified']
    list_filter = ('owner','created', 'modified')


class WebCodeAdmin(admin.ModelAdmin):
    list_display = ['code',]


class OtherCodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'lang']
    list_filter = ('lang',)

admin.site.register(SupportedLanguages,SupportedLanguagesAdmin)
admin.site.register(Code, CodeAdmin)
admin.site.register(WebCode, WebCodeAdmin)
admin.site.register(OtherCode, OtherCodeAdmin)
