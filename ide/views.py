from django.shortcuts import render
from django.http import JsonResponse, HttpResponseNotFound
from .models import codes
import requests, json, os
from .models import SupportedLanguages
from .forms import MediaForm



RUN_URL = u"https://api.jdoodle.com/v1/execute"
clientSecret = "28c60d0e09ddd9d82ac4d48758a679fe0051c7bf82819590cfd22a068bed1ad5"
clientId = "8bd8f1555d1454df0f7df8cacf9f4eb9"

permitted_languages = ["c", "cpp","java","ruby", "php", "python2","python3","r", "swift",
 "csharp", "sql"]


def ide_index(request):

    languages = SupportedLanguages.objects.all()
    return render(request,'ide_index.html', {'languages': languages })

def media(language):
    """"
    add the   language script

    """
    return forms.Media(js={'all' :
    'codemirror/mode/'+language+'/'+language+'.js'})

def main_editor(request, language):
    template = ''
    context = {}
    language_mode= ''
    if language == 'frontend-editor':
        template = 'ide/forntend_ide_form.html'
        context = {'language_mode' : language_mode}
        language_mode = MediaForm.media(language)
    else:
        if language in permitted_languages:
            source = None
            output = None

            if request.method == "POST":
                source = request.POST.get('code')

                data = {
                "clientId": clientId,
                "clientSecret": clientSecret,
                "script":source,
                "language":language,
                "versionIndex":"1"}

                r = requests.post(RUN_URL,  json=data)
                output = r.json()['output']
            import re
            language = "".join(re.findall("[a-zA-Z]+", language))
            language_mode = MediaForm.media(language)
            template = 'ide/main_ide_form.html'
            context = {'output' : output , 'source': source, 'language_mode' : language_mode}
        else:
            return HttpResponseNotFound()
    context['language'] = language
    return render(request,template,context);
