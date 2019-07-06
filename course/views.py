from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.shortcuts import render, redirect,HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from django.contrib.auth.models import User
from .models import( Subject, Course, Module, Content, ContentNote
,TakenCourse, TakenModule,TakenContent)
from accounts.models import Question, Answer, StudentAnswer
from .forms import ContentNoteForm, CourseForm
from accounts.models import Student, Quiz, Stage



def subjects(request):
    subject = Subject.objects.all()

    return render(request,'course/subjects_form.html',{'subject' : subject})


@login_required
def courses(request, subject):
     #actual_subject = Subject.objects.get(slug = subject)
    subject_course = Course.objects.filter(subject__slug = subject )
    middle_course =subject_course[:(subject_course.count())/2]
    top_course =subject_course[(subject_course.count()/2):(subject_course.count()*3)/4]
    bottom_course =subject_course[((subject_course.count()*3)/4):]

    print(middle_course.count())
    print(bottom_course.count())
    print(top_course.count())

    views = []
    student_taken_course = TakenCourse.objects.filter(student = request.user.student).values_list('course', flat=True)

    for course in subject_course :
        views.append(TakenCourse.objects.filter(course = course ).count())


    return render(request,'course/course_form.html',
    {'subject':subject ,'middle_course':middle_course, 'bottom_course':bottom_course,'top_course':top_course,  'student_taken_course':student_taken_course
         ,'views' : views  })

@login_required
def modules(request, subject, course):
    actual_course = Course.objects.get(slug = course)
    course_module = Module.objects.filter(course = actual_course)
    check_taken_course = TakenCourse.objects.filter(student =request.user.student, course=actual_course)
    completed_taken_module = TakenModule.objects.filter(student =request.user.student , course=actual_course, completed= True)
    last_taken_module = completed_taken_module.last()

    completed_taken_module_count = 0;
    course_module_count = 0;

    if check_taken_course.count()==0:
        new_taken_course = TakenCourse.objects.create(student = request.user.student, course=actual_course,  subject= actual_course.subject, completed = False)
    completed_module = ''
    next_module  = ''
    student_taken_module  = ''
    if last_taken_module:
        if course_module:
            completed_module = Module.objects.filter(course =actual_course , pk__lte = last_taken_module.module.pk)

            next_module = Module.objects.filter( course=actual_course, pk__gt = completed_module.last().pk ).first()
            student_taken_module = TakenModule.objects.filter(student =request.user.student, course=actual_course).values_list('module', flat=True)

            completed_taken_module_count = completed_taken_module.count()
            course_module_count = course_module.count()
            if  completed_taken_module.count()  == course_module.count():
                next_module = Module.objects.filter( course=actual_course).first()
                TakenCourse.objects.filter(student = request.user.student, course=actual_course,  subject= actual_course.subject).update(completed = True)
                request.user.student.exp += 50
                request.user.student.save()

    else:
        next_module = Module.objects.first()
    return render(request,'course/modules_form.html', {'course_module_count':course_module_count,'completed_taken_module_count':completed_taken_module_count,'student_taken_module':student_taken_module,
    'course':actual_course ,'course_module':course_module, 'completed_module': completed_module ,
    'completed_taken_module':completed_taken_module, 'next_module': next_module })

@login_required

def contents(request, course, module):
    current_module= Module.objects.get(slug = module)
    module_content= Content.objects.filter(module__slug = module)
    count_content = module_content.count()
    check_taken_module = TakenModule.objects.filter(student = request.user.student, module=current_module )
    start_first_content = None
    if module_content:
        start_first_content = module_content.order_by('id')[0]

    student_taken_content = TakenContent.objects.filter(student = request.user.student, module= current_module).values_list('id', flat =True)
    count_taken_content = student_taken_content.count()

    check_taken_module = TakenModule.objects.filter(student = request.user.student, module=current_module )
    if check_taken_module.count() == 0:
        new_taken_module = TakenModule.objects.create(student=request.user.student, module=current_module, course = current_module.course , completed = False)
    #if count_taken_content == module_content.count():
       #TakenModule.objects.filter(student=request.user.student, module=current_module , course = current_module.course).update(completed = True)

    return render(request,'course/contents_form.html',  {'module':module ,'count_content':count_content
        ,'student_taken_content': student_taken_content, 'start_first_content':start_first_content,  })


@login_required
def learn(request, module, content):
    content_learn= Content.objects.get(slug = content)
    current_student = Student.objects.get(user=request.user)
    print(module)
    check_taken_content = TakenContent.objects.filter(student = current_student, content=content_learn, module = content_learn.module).exists()
    if check_taken_content is not True:
        new_taken_content =  TakenContent.objects.create(student = current_student, content=content_learn, module = content_learn.module)
        request.user.student.exp += 1
        request.user.student.save()

    note_form = ContentNoteForm()
    if request.method == "POST":
            note_form = ContentNoteForm(request.POST)
            if note_form.is_valid() :
                form = note_form.save(commit=False)
                if ContentNote.objects.filter(user = request.user, content = content_learn).count()==0:

                    form.content = Content.objects.get(slug =content)
                    form.note = request.POST.get('note')
                    form.user = request.user
                    form.save()
                else:
                    ContentNote.objects.filter(user = request.user, content = content_learn).update(note = note_form.cleaned_data['note'])
    return render(request,'course/learn_form.html',
    {'content':content ,'content_learn':content_learn,'note_form' : note_form ,
      })
@login_required

def learn_question(request, module, content, question):

    this_question = Question.objects.get(pk = question)
    this_content = Content.objects.get(question = this_question)
    print(TakenContent.objects.filter(student = request.user.student, content = this_content))
    if  TakenContent.objects.filter(student = request.user.student, content = this_content).exists() is False:
        return HttpResponse('you can\'t access this question yet')
    this_question_answers = Answer.objects.filter(question = this_question)
    this_question_right_answers_count = Answer.objects.filter(question = this_question, is_correct = True).count()

    result = None
    if request.method == "POST":
        count = 0
        result= True
        student_answers = request.POST.getlist('answer')
        for answer_id in student_answers:

            answered = Answer.objects.get(id = answer_id)
            if answered.is_correct == True:
                count+=1
            else :
                result = False

        if this_question_right_answers_count == count and result == True:

            if StudentAnswer.objects.filter(student= request.user.student , question=this_question, stage=this_question.stage).count()==0:
                StudentAnswer.objects.create(student= request.user.student , question=this_question, stage=this_question.stage)
                request.user.student.exp+= answered.question.point
                request.user.student.save()
            next_content = Content.objects.filter(module__slug= module, order__gt = this_content.order).first()
            if next_content is not None:
                return redirect(reverse('learn', args=(next_content.module.slug, next_content.slug)))
            else:
                TakenModule.objects.filter(student=request.user.student, module=this_content.module , course = this_content.module.course).update(completed = True)
                request.user.student.exp += 20
                request.user.student.save()
                return redirect(reverse('modules', args=(this_content.module.course.subject.slug, this_content.module.course.slug)))
        else:
            result = False
    return render(request, 'course/content_question_form.html',{'result': result, 'this_question' : this_question,
        'this_question_answers' : this_question_answers,})

def add_course(request, subject):
    course_form = CourseForm()
    if request.method == 'POST':
        course_form = CourseForm(request.POST)


        if course_form.is_valid():
            course = Course(
              owner = request.user,
              subject = Subject.objects.get(slug= subject),
              title = course_form.cleaned_data['title'],
              overview = course_form.cleaned_data['overview']
            )
            check_if_student_can_add =  False
            count_user_suggested_courses_day =  Course.objects.filter( owner = request.user, created = timezone.now().date()).count()
            if( request.user.student.rank.name > 8 and  count_user_suggested_courses_day == 0):
                course.save()
                course.tags.set(request.POST.getlist('tags'))
            else:
                course_form.add_error(None,'cant Suggest a course you reach the limit or you rank is less than Mage ')



    return render(request, 'course/add_course_form.html', {'course_form' : course_form})

def add_module(request, course):
    return render(request, 'course/add_module_form.html', {})
