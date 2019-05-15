from django.shortcuts import render,redirect, render_to_response
from django.http import JsonResponse, HttpResponseNotFound, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
import requests, json, os
from .models import SupportedLanguages,Code,WebCode,OtherCode,Vote
from .forms import MediaForm



RUN_URL = u"https://api.jdoodle.com/v1/execute"
clientSecret = "28c60d0e09ddd9d82ac4d48758a679fe0051c7bf82819590cfd22a068bed1ad5"
clientId = "8bd8f1555d1454df0f7df8cacf9f4eb9"

permitted_languages = ["c", "cpp","java","ruby", "php", "python2","python3","r", "swift",
 "csharp", "sql"]


def ide_index(request):
    languages = SupportedLanguages.objects.order_by('?')
    web_codes = WebCode.objects.order_by('?')[:15]
    other_codes = OtherCode.objects.order_by('?')[:15]

    return render(request,'ide_index.html', {'languages': languages, 'web_codes':web_codes,
    'other_codes':other_codes })

def media(language):
    """"
    add the   language script

    """
    return forms.Media(js={'all' :
    'codemirror/mode/'+language+'/'+language+'.js'})


@login_required
def main_editor(request, language):
    template = ''
    context = {}
    language_mode= ''

    """
    Web Programming languages

    """
    if language == 'frontend-editor':
        template = 'ide/forntend_ide_form.html'
        html = '<h1>a</h1>'
        css = 'h1 { color : red}'
        js = """var spanElements = document.getElementsByTagName('h1');
        for (var i = 0; i < spanElements.length; i++) {
        spanElements[i].style.color = 'green';
        }"""
        context = {'language_mode' : language_mode, 'html' : html, 'css' : css, 'js' : js}
        language_mode = MediaForm.media(language)


        if request.method == "POST":
            if request.POST.get('html'):
                this_code = Code.objects.create(title = request.POST.get('title'),owner = request.user.student)
                web_code = WebCode.objects.create(code = this_code,  css = request.POST.get('css'),
                html= request.POST.get('html'), js = request.POST.get('js') )
                return redirect(ide_index)
            else:
                context['err'] = 'cant save empty code'

    else:
        if language in permitted_languages:
            source = None
            output = None
            if request.method == "POST":
                source = request.POST.get('code')
                if 'run' in request.POST:
                    if source:
                        data = {
                        "clientId": clientId,
                        "clientSecret": clientSecret,
                        "script":source,
                        "language":language,
                        "versionIndex":"1"}

                        r = requests.post(RUN_URL,  json=data)
                        output = r.json()['output']
                if 'save' in request.POST:
                    if source:
                        this_code = Code.objects.create(owner = request.user.student, title = request.POST.get('title'))
                        supprted_language = SupportedLanguages.objects.get(name = language)
                        other_code = OtherCode.objects.create(code = this_code, content = source, lang = supprted_language)
                        return redirect(ide_index)
                    else:
                        context['err'] = 'cant save empty code'
            import re
            language = "".join(re.findall("[a-zA-Z]+", language))
            language_mode = MediaForm.media(language)
            template = 'ide/main_ide_form.html'
            context = {'output' : output , 'source': source, 'language_mode' : language_mode}


        else:
            return HttpResponseNotFound()
    context['language'] = language
    return render(request,template,context);


@login_required
def share_frontend(request,slug,pk):
    code = WebCode.objects.get(code__slug = slug, code__pk = pk)
    voted_check = Vote.objects.filter(code= code.code, owner=request.user.student)
    if request.method == "POST":
        if 'update' in request.POST:
            WebCode.objects.filter(code__pk = pk).update( html = request.POST.get('html'),
                css = request.POST.get('css'),
                 js = request.POST.get('js'))
            return redirect(ide_index)
        """
        if 'vote' in request.POST:
            # check if user can vote

            if voted_check.count() > 0:
                voted_check.delete()
                code.code.owner.exp -= 2
                code.code.owner.save()
            else:
                Vote(code= code.code, owner=request.user.student).save()
                code.code.owner.exp += 2
                code.code.owner.save()
        """
    voted_check_id = ""
    if voted_check:
        voted_check_id = list(voted_check.values_list('pk'))[0][0]
    return render(request, 'ide/share_frontend_form.html',{'voted_check':voted_check_id, 'code': code})



@login_required
def share_code(request,slug,pk):
    other_code = OtherCode.objects.get(code__pk = pk)
    voted_check = Vote.objects.filter(code= other_code.code, owner=request.user.student)
    language =other_code.lang.name
    source = None
    output = None
    if request.method == "POST":
        source = request.POST.get('code')
        if 'run' in request.POST:
            if source:
                data = {
                "clientId": clientId,
                "clientSecret": clientSecret,
                "script":source,
                "language":language,
                "versionIndex":"1"}

                r = requests.post(RUN_URL,  json=data)
                output = r.json()['output']
        if 'save' in request.POST:
            if source:
                OtherCode.objects.filter(code__pk = pk).update(content = source)
                return redirect(ide_index)
            else:
                context['err'] = 'cant save empty code'
        if 'vote' in request.POST:
            # check if user can vote

            if voted_check.count() > 0:
                voted_check.delete()
                other_code.code.owner.exp -= 2
                other_code.code.owner.save()
            else:
                Vote(code= other_code.code, owner=request.user.student).save()
                other_code.code.owner.exp += 2
                other_code.code.owner.save()
    import re
    language = "".join(re.findall("[a-zA-Z]+", language))
    language_mode = MediaForm.media(language)
    voted_check_id = ""
    if voted_check:
        voted_check_id = list(voted_check.values_list('pk'))[0][0]
    context = {'voted_check':voted_check_id ,'output' : output , 'source': source, 'language_mode' : language_mode, 'other_code' : other_code}

    context['language'] = language

    return render(request, 'ide/share_code_form.html',context)


"""
REST API

"""

from .serializers import VoteSerializer
from rest_framework import viewsets


class VoteView(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class  = VoteSerializer
    http_method_names = ['get', 'post', 'head', 'delete', 'patch']
