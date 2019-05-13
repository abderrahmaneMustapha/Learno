from django.contrib import admin
from .models import SupportedLanguages,Code,WebCode,OtherCode,Vote




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
class VoteAdmin(admin.ModelAdmin):
    list_display = ['code', 'owner']
    list_filter = ('code',)

admin.site.register(SupportedLanguages,SupportedLanguagesAdmin)
admin.site.register(Code, CodeAdmin)
admin.site.register(WebCode, WebCodeAdmin)
admin.site.register(OtherCode, OtherCodeAdmin)
admin.site.register(Vote, VoteAdmin)
