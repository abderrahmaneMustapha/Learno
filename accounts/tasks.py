# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task,Celery
from .models import calculate_rank
from learno.celery import app



@shared_task
def calculate_rank_task():
    print('q')
    calculate_rank()
