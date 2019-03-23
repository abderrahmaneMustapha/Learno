from django.shortcuts import render
from django.http import JsonResponse, HttpResponseForbidden
from .models import codes
import requests, json, os

COMPILE_URL = "https://api.hackerearth.com/v3/code/compile/"
RUN_URL = "https://api.hackerearth.com/v3/code/run/"

# access config variable
DEBUG = (os.environ.get('HACKIDE_DEBUG') != None)
# DEBUG = (os.environ.get('HACKIDE_DEBUG') or "").lower() == "true"
CLIENT_SECRET = "99ecf294ff455cb99761af79f08a7e8a8e37619a"

permitted_languages = ["C", "CPP","JAVA", "JAVASCRIPT", "PERL", "PHP", "PYTHON","RUBY"]


"""
Check if source given with the request is empty
"""
def source_empty_check(source):
  if source == "":
    response = {
      "message" : "Source can't be empty!",
    }
    return JsonResponse(response, safe=False)

"""
Check if lang given with the request is valid one or not
"""
def lang_valid_check(lang):
  if lang not in permitted_languages:
    response = {
      "message" : "Invalid language - not supported!",
    }
    return JsonResponse(response, safe=False)

"""
Handle case when at least one of the keys (lang or source) is absent
"""
def missing_argument_error():
  response = {
    "message" : "ArgumentMissingError: insufficient arguments for compilation!",
  }
  return JsonResponse(response, safe=False)



def ide_index(request):
    return render(request,'ide/ide_index.html',{});


"""
Method catering to AJAX call at /ide/compile/ endpoint,
makes call at HackerEarth's /compile/ endpoint and returns the compile result as a JsonResponse object
"""
def compile_code(request):
    if request.is_ajax():
        try:
          source = request.POST['source']
          # Handle Empty Source Case
          source_empty_check(source)

          lang = request.POST['lang']
          # Handle Invalid Language Case
          lang_valid_check(lang)

        except KeyError:
          # Handle case when at least one of the keys (lang or source) is absent
          missing_argument_error()

        else:
          compile_data = {
            'client_secret': CLIENT_SECRET,
            'async': 0,
            'source': source,
            'lang': lang,
          }

          r = requests.post(COMPILE_URL, data=compile_data)
          return JsonResponse(r.json(), safe=False)
    else:
        return HttpResponseForbidden();


def run_code(request):
    if request.is_ajax():
        try:
          source = request.POST['source']
          # Handle Empty Source Case
          source_empty_check(source)

          lang = request.POST['lang']
          # Handle Invalid Language Case
          lang_valid_check(lang)

        except KeyError:
          # Handle case when at least one of the keys (lang or source) is absent
          missing_argument_error()

        else:
          # default value of 5 sec, if not set
          time_limit = request.POST.get('time_limit', 5)
          # default value of 262144KB (256MB), if not set
          memory_limit = request.POST.get('memory_limit', 262144)

          run_data = {
            'client_secret': CLIENT_SECRET,
            'async': 0,
            'source': source,
            'lang': lang,
            'time_limit': time_limit,
            'memory_limit': memory_limit,
          }

          # if input is present in the request
          code_input = ""
          if 'input' in request.POST:
            run_data['input'] = request.POST['input']
            code_input = run_data['input']

          """
          Make call to /run/ endpoint of HackerEarth API
          and save code and result in database
          """
          r = requests.post(RUN_URL, data=run_data)
          r = r.json()
          cs = ""
          rss = ""
          rst = ""
          rsm = ""
          rso = ""
          rsstdr = ""
          try:
            cs = r['compile_status']
          except:
            pass
          try:
            rss=r['run_status']['status']
          except:
            pass
          try:
            rst = r['run_status']['time_used']
          except:
            pass
          try:
            rsm = r['run_status']['memory_used']
          except:
            pass
          try:
            rso = r['run_status']['output_html']
          except:
            pass
          try:
            rsstdr = r['run_status']['stderr']
          except:
            pass

          code_response = codes.objects.create(
            code_id = r['code_id'],
            code_content = source,
            lang = lang,
            code_input = code_input,
            compile_status = cs,
            run_status_status = rss,
            run_status_time = rst,
            run_status_memory = rsm,
            run_status_output = rso,
            run_status_stderr = rsstdr
          )
          code_response.save()
          return JsonResponse(r, safe=False)
    else:
        return HttpResponseForbidden()

def saved_code_view(request, code_id):
  result = codes.objects(code_id=code_id)
  result = result[0].to_json()
  result = json.loads(result)

  code_content = result['code_content']
  lang = result['lang']
  code_input = result['code_input']
  compile_status = str(result['compile_status'].encode('utf-8')).decode('utf-8')
  run_status_status = result['run_status_status']
  run_status_time = result['run_status_time']
  run_status_memory = result['run_status_memory']
  run_status_output = result['run_status_output']
  run_status_stderr = result['run_status_stderr']

  return render(request, 'ide/ide_index.html', {
    'code_content': code_content,
    'lang': lang,
    'inp': code_input,
    'compile_status': compile_status,
    'run_status_status': run_status_status,
    'run_status_time': run_status_time,
    'run_status_output': run_status_output,
    'run_status_memory': run_status_memory,
    'run_status_stderr': run_status_status
  })
