from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.models import User
from background_task.models import  Task, TaskQuerySet
from background_task.models_completed import CompletedTask

from .forms import StudentForm, UserForm ,AnswerForm, EditUserForm
from .models import (Student, Tag, Quiz, Question, Answer,StudentAnswer,Badge,
TakenQuiz, Stage, CompletedStage, LastStudentAnswer, StudentLevel)
from course.models import TakenCourse, TakenModule, TakenContent,Subject
    #######################
    # background task
from background_task import background, tasks
from django.contrib.auth.models import User

@background
def hello(student_name):
    # lookup user by id and send them a message
    this_user = User.objects.get(username = student_name)
    Student.calculate_rank(this_user.student)
    print(this_user.student.rank)

########################


def home(request):
    subject = Subject.objects.all()
    """
    CompletedTask.objects.all().delete()
    Task.objects.all().delete()
    
    """
    if request.user.is_authenticated:
        student = Student.objects.only('pk').get(user = request.user)
        print(student)
        hello(str(student), repeat= 5 , repeat_until = None)
    return render(request,'home.html',{'subject' : subject})


def signup(request):
    user_form = UserForm()
    student_form = StudentForm()

    if request.method == "POST":
            user_form = UserForm(request.POST)
            student_form = StudentForm(request.POST, request.FILES)
            if user_form.is_valid() and student_form.is_valid():
                new_user = User.objects.create_user(username = request.POST.get('username'),
                password = request.POST.get('password'), email = request.POST.get('email'))

                new_student = student_form.save(commit=False)
                new_student.user = new_user
                new_student.save()
                new_student.interests.set(request.POST.getlist('interests',))
                login_user =  authenticate(
                    username = user_form.cleaned_data["username"],
                    password = user_form.cleaned_data["password"]
                )
                if login_user is not None:
                    login(request, login_user)

                return redirect(profile)

    return render(request,'registration/signup.html',{
            'user_form' : user_form,
            'student_form' : student_form,
    })

@login_required
def edit_profile(request):
    user_form = EditUserForm(instance=request.user)
    student_form = StudentForm(instance=request.user.student)

    if request.method == "POST":
            user_form = EditUserForm(request.POST, instance=request.user)
            student_form = StudentForm(request.POST, request.FILES, instance=request.user.student)
            if user_form.is_valid() and student_form.is_valid():
                new_user = User.objects.get(username = request.user.username)
                new_student = student_form.save(commit=False)
                new_student.user = new_user
                new_student.save()
                new_student.interests.set(request.POST.getlist('interests',))

                return redirect(profile)

    return render(request, 'accounts/edit_profile.html', {
            'user_form' : user_form,
            'student_form' : student_form,
    })




@login_required
def profile(request):
    interests = request.user.student.interests.all()
    taken_course = TakenCourse.objects.filter(student = request.user.student )
    taken_module = TakenModule.objects.filter(student = request.user.student)
    taken_content = TakenContent.objects.filter(student = request.user.student)
    level = Student.calculate_level(request.user.student)
    Student.calculate_rank(request.user.student)
    return render(request, 'accounts/profile.html',{'interests' : interests ,
        'taken_course' : taken_course, 'taken_module' : taken_module
        , 'taken_content' : taken_content, 'level':level })

def profiles(request,user):
    this_user = User.objects.get(username = user)
    this_student = Student.objects.get(user = this_user)
    print(this_student.interests.all())
    return render(request, 'accounts/profiles.html', {'this_student' : this_student})

def leaderboard_view(request):
    all_students = Student.objects.order_by('-exp')[:20]
    print( "all students" + str(all_students) + "\n")
    student_high_rank =  Student.objects.filter(exp__gte = request.user.student.exp )[:5]
    print(student_high_rank)
    student_less_rank =  Student.objects.filter(exp__lte = request.user.student.exp ).exclude(user = request.user)[:5]
    print(student_less_rank)

    return render(request, 'accounts/leaderboard.html', {'all_students': all_students})
@login_required
def quizzes_view(request):
    quizzes = Quiz.objects.all()
    views = []
    for quiz in quizzes:
        views.append(TakenQuiz.objects.filter(quiz = quiz).count())

    taken_quiz = TakenQuiz.objects.filter(student = request.user.student).values_list('quiz', flat=True)
    return render(request, 'quizzes/quizzes_form.html',{'quizzes':quizzes,
                                    'taken_quiz':taken_quiz , 'views' : views})
@login_required
def stages_view(request,quiz):
    actual_quiz = Quiz.objects.get(name= quiz)
    stages = Stage.objects.filter(quiz = actual_quiz )
    if TakenQuiz.objects.filter(student =request.user.student, quiz = actual_quiz).count()== 0:
        taken_quiz = TakenQuiz.objects.create(student =request.user.student, quiz = actual_quiz , last_entr = timezone.now() )
    else :
        taken_quiz = TakenQuiz.objects.filter(student =request.user.student, quiz = actual_quiz).update(last_entr = timezone.now() )

    completed_stages = CompletedStage.objects.filter(student = request.user.student, quiz=actual_quiz).values_list('stage' , flat=True)

    return render(request, 'quizzes/stages_form.html',{'stages':stages,
                            'completed_stages' : completed_stages})


@login_required
def questions_view(request,stage):
    actual_stage = Stage.objects.get(name=stage)
    questions = Question.objects.filter(stage = actual_stage)
    questions_count = questions.count()
    answered = ''
    current_student_exp = Student.objects.get(user = request.user)

    #collect the correct answer of actual student
    correct_answers = StudentAnswer.objects.filter(student = request.user.student, stage=actual_stage).values_list('question', flat=True)
    correct_answers_count = correct_answers.count()

    if questions_count != 0:
        if correct_answers_count == questions_count  :
            if CompletedStage.objects.filter(student = request.user.student , stage = actual_stage , quiz = actual_stage.quiz).count() == 0:
                CompletedStage.objects.create(student = request.user.student , stage = actual_stage ,quiz = actual_stage.quiz , score=1)
                current_student_exp.exp+= 1

    answers = Answer.objects.all()

    if request.method == "POST":
        result=False
        student_answer = request.POST.getlist("answer")
        for s_an in student_answer:
            result=True
            answered = Answer.objects.get(id=s_an)
            if answered.is_correct == False:
                result = False
                break
        if  LastStudentAnswer.objects.filter(student= request.user.student , question=answered.question, stage=answered.question.stage).count()==0:
            LastStudentAnswer.objects.create(student= request.user.student , question=answered.question, stage=answered.question.stage, result = result , last_entr = timezone.now())

        else:
            LastStudentAnswer.objects.filter(student= request.user.student , question=answered.question, stage=answered.question.stage).update(result= result , last_entr=timezone.now())

        if result == True:
             if StudentAnswer.objects.filter(student= request.user.student , question=answered.question, stage=answered.question.stage).count()==0:
                StudentAnswer.objects.create(student= request.user.student , question=answered.question, stage=answered.question.stage)

                current_student_exp.exp+= answered.question.point
                current_student_exp.save()



    return render(request, 'quizzes/questions_form.html',{ 'stage' : stage,'questions':questions
    ,'answers' : answers, 'correct_answers':correct_answers, 'correct_answers_count': correct_answers_count ,
     'questions_count':questions_count,})

def stage_result_view(request,stage, stage_result):
    actual_stage = Stage.objects.get(name=stage)
    last_student_result = LastStudentAnswer.objects.filter(student= request.user.student ,stage=actual_stage, result = True).count()

    questions_number  = Question.objects.filter(stage = actual_stage).count()

    return render(request, 'quizzes/stage_result_form.html', {'last_student_result' : last_student_result ,
                        'questions_number' : questions_number })
