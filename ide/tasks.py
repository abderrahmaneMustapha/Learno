# Create your tasks here
from celery import shared_task
from accounts.models import Badge,TakenBadge
from learno.celery import app

def calculate_votebadges_task(vote, current_student):
    if TakenBadge.objects.filter(badge__name = 'junior coder', student = current_student).count() == 0:
        print(vote.count())
        if vote.count() >= 5:
            badge  = Badge.objects.get(name = 'junior coder')
            taken_badge = TakenBadge.objects.create(student = current_student, badge= badge)
            current_student.exp += badge.point
            current_student.save()
    if TakenBadge.objects.filter(badge__name = 'amateur coder', student = current_student).count() == 0:
       if vote.count() >=20:
            badge = Badge.objects.get(name = 'amateur coder')
            taken_badge = TakenBadge.objects.create(student = current_student, badge = badge)
            current_student.exp += badge.point
            current_student.save()
