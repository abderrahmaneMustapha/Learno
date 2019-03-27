from django.db import models

class codes(models.Model):
    code_id = models.TextField( max_length=500)
    code_content =models.TextField( max_length=500)
    lang = models.TextField( max_length=500)
    code_input = models.TextField( max_length=500)
    compile_status=  models.TextField( max_length=500)
    run_status_status= models.TextField( max_length=500)
    run_status_time= models.TextField( max_length=500)
    run_status_memory= models.TextField( max_length=500)
    run_status_output= models.TextField( max_length=500)
    run_status_stderr= models.TextField( max_length=500)

class SupportedLanguages(models.Model):
    name = models.TextField( max_length=500)
    created = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.name
