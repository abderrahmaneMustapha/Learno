from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.models import User

from django.views.decorators.cache import cache_page

from .forms import StudentForm, UserForm, EditUserForm,SearchForm,ContactUs
from .models import ( Student, Tag, Quiz, Question, Answer,StudentAnswer,Badge,
TakenQuiz,TakenBadge, Stage, CompletedStage, LastStudentAnswer, StudentLevel, calculate_rank)

from course.models import ContentNote,  TakenCourse, TakenModule, TakenContent,Subject,Course,Subject,Module
from . serializers import StudentSerializer

from django.core import serializers


def home(request):

    """
    COURSES

    """
    all_courses = Course.objects.filter(approved = True)
    suggested_courses = all_courses.order_by('?')[:6]


    """
    SBJECTS

    """
    all_subject= Subject.objects.filter(approved = True)

    """
    this is how we reverse ForeignKey search
    print(Course.objects.filter(subject__title = 'Programming language').count())
    """
    #
    #"data = serializers.serialize("json", Subject.objects.all(), fields=('title'))
    #print(data)



    """
    Seach queryset

    """


    search_query = None
    search_form = SearchForm()
    if request.method == "POST":
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            from django.contrib.postgres.search import SearchVector, TrigramSimilarity
            search_for = search_form.cleaned_data.get('search')
            print(search_for)
            search_query = Course.objects.annotate(
                search = SearchVector('title')+
                SearchVector('subject__title'),
            ).filter(search__icontains= search_for)

            print(search_query)

    return render(request,'home.html',{'all_subject' : all_subject, 'search_query': search_query,
       'search_form':search_form, 'all_courses':all_courses,'suggested_courses' : suggested_courses})



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
                else:
                    student_form.add_error(None, 'Cant signup')
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
            user_form =  EditUserForm(request.POST, instance=request.user)
            student_form = StudentForm(request.POST, request.FILES, instance=request.user.student)
            if user_form.is_valid() and student_form.is_valid():
                user_form.save()
                student_form.save()

                return redirect(profile)

    return render(request, 'accounts/edit_profile.html', {
            'user_form' : user_form,
            'student_form' : student_form,
    })



from ide.models import Vote
from ide.tasks import calculate_votebadges_task
@login_required
def profile(request):
    taken_badge = TakenBadge.objects.filter(student = request.user.student)
    interests = request.user.student.interests.all()

    #calcuate user badges
    vote = Vote.objects.filter(code__owner = request.user.student)
    current_student = request.user.student
    calculate_votebadges_task(vote, current_student)

    #get the user taken course and user created course number
    taken_course = TakenCourse.objects.filter(student = request.user.student )
    total_course =  Course.objects.filter(owner = request.user).count()

    #get completed modules and total modules for each course
    #number of completed modules in each course
    skills_comp= []
    #number of modules in each course
    skills_mod = []
    for course in taken_course:
        temp = TakenModule.objects.filter(student = request.user.student, course__title= course, completed = True).count()
        temp0 = Module.objects.filter(course__title= course).count()
        skills_mod.append(temp0)
        skills_comp.append(temp)


    #get the total number of the codes
    from ide.models import WebCode,OtherCode
    web_code = WebCode.objects.filter(code__owner = request.user.student).order_by('?')
    other_code = OtherCode.objects.filter(code__owner = request.user.student).order_by('?')
    total_code = web_code.count() + other_code.count()

    #get all the student answered questions
    total_answers = StudentAnswer.objects.filter(student = request.user.student).count()

    level = Student.calculate_level(request.user.student)

    next_level_exp = (4*(level+1))*(4*(level+1))

    #get all student notes
    taken_note = ContentNote.objects.filter(user = request.user)
    #providers = request.user.social_auth.values_list('provider')
    return render(request, 'accounts/profile.html',{'skills_mod':skills_mod, 'skills_comp':skills_comp, 'other_code': other_code[:3], 'web_code': web_code[:3],
    'interests' : interests ,'total_code' : total_code,
    'total_answers':total_answers, 'taken_course' : taken_course,
    'level':level,'next_level_exp':next_level_exp, 'total_course' : total_course,
    'taken_note':taken_note, 'taken_badge':taken_badge})



def profiles(request,user):
    this_student = Student.objects.get(user__username = user)
    taken_badge = TakenBadge.objects.filter(student = this_student)
    interests = this_student.interests.all()
    #calcuate voting badges
    vote = Vote.objects.filter(code__owner = this_student)
    current_student = this_student
    calculate_votebadges_task(vote, current_student)
    #get the user taken course and user created course number
    taken_course = TakenCourse.objects.filter(student = this_student )
    total_course =  Course.objects.filter(owner = this_student.user).count()
    #get completed modules and total modules for each course
    #number of completed modules in each course
    skills_comp= []
    #number of modules in each course
    skills_mod = []
    for course in taken_course:
        temp = TakenModule.objects.filter(student = this_student, course__title= course, completed = True).count()
        temp0 = Module.objects.filter(course__title= course).count()
        skills_mod.append(temp0)
        skills_comp.append(temp)


    #get the total number of the codes
    from ide.models import WebCode,OtherCode
    web_code = WebCode.objects.filter(code__owner = this_student).order_by('?')
    other_code = OtherCode.objects.filter(code__owner = this_student).order_by('?')
    total_code = web_code.count() + other_code.count()

    #get all the student answered questions
    total_answers = StudentAnswer.objects.filter(student = this_student).count()

    level = Student.calculate_level(this_student)
    next_level_exp = (4*(level+1))*(4*(level+1))
    return render(request, 'accounts/profiles.html', {'this_student' : this_student, 'skills_mod':skills_mod, 'skills_comp':skills_comp, 'other_code': other_code[:3], 'web_code': web_code[:3],
    'interests' : interests ,'total_code' : total_code,
    'total_answers':total_answers, 'taken_course' : taken_course, 'level':level,'next_level_exp':next_level_exp,
    'total_course' : total_course, 'taken_badge':taken_badge })

@login_required
def leaderboard_view(request):
    all_students = Student.objects.order_by('-exp')[:10]
    student_high_rank =  Student.objects.filter(exp__gte = request.user.student.exp )[:2]
    student_less_rank =  Student.objects.filter(exp__lte = request.user.student.exp ).exclude(user = request.user)[:2]
    king = all_students[0]
    return render(request, 'accounts/leaderboard.html', {'king':king, 'all_students': all_students})
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



def about(request):
    admins = Student.objects.filter(user__is_staff = True)
    print(admins)
    return render(request, 'about.html', { })

def contact(request):
    contact_us = ContactUs()
    if request.method == "POST":
        contact_us = ContactUs(request.POST)
        if contact_us.is_valid():
            from django.core.mail import send_mail
            send_mail(
                contact_us.cleaned_data.get('subject'),
                str(contact_us.cleaned_data.get('name'))+"\n"
                +str(contact_us.cleaned_data.get('phone')) + "\n"
                +str(contact_us.cleaned_data.get('email')) + "\n"
                +str(contact_us.cleaned_data.get('text')),
                 "abderrahmanemustapha030898@gmail.com",
                ['abderrahmanemustapha030898@gmail.com','salaheddineguenadza14@gmail.com','alilougt@gmail.com'],
                fail_silently=False,
            )

    return render(request, 'contact.html', {'contact_us': contact_us,})
######## REST API ########
from rest_framework import permissions
from rest_framework import viewsets

class StudentView(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
