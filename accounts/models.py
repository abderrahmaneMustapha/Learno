from django.db import models
from django.contrib.auth.models import User
from colorful.fields import RGBColorField
User._meta.get_field('email')._unique = True

class Tag(models.Model):
    name = models.CharField(max_length=30)
    color = RGBColorField(max_length=7, default='#007bff')

    def __str__(self):
        return self.name


class Quiz(models.Model):
    name = models.CharField(max_length=255)
    tags = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='quizzes' )
    point = models.IntegerField(null=True, default=0)
    def __str__(self):
        return self.name
class Stage(models.Model):
    name = models.CharField(max_length=255)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='stages')
    def __str__(self):
        return self.name

class Question(models.Model):
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, related_name='questiones')
    text = models.CharField('Question', null=True,blank=True,max_length=300)
    point = models.IntegerField(null=True, default=0)

    def __str__(self):
        return self.text

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField('Answer', max_length=255)
    is_correct = models.BooleanField('Correct answer', default=False)

    class Meta:
        unique_together = [
            # no duplicated text per question
            ("question", "text"),        ]


    def __str__(self):
        return self.text

class Badge(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=300)
    point_required = models.FloatField()

class Level(models.Model):
    exp = models.PositiveIntegerField(default=1)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='student')
    photo = models.ImageField(upload_to='picture_profile/',default='default-96.png',blank=True)
    quizzes = models.ManyToManyField(Quiz,blank=True, through='TakenQuiz')
    interests = models.ManyToManyField(Tag,blank=True, related_name='interested_students')
    exp = models.PositiveIntegerField(blank=True,default=1)


    def get_unanswered_questions(self, quiz):
        answered_questions = self.quiz_answers \
            .filter(answer__question__quiz=quiz) \
            .values_list('answer__question__pk', flat=True)
        questions = quiz.questions.exclude(pk__in=answered_questions).order_by('text')
        return questions

    def __str__(self):
        return self.user.username

#this Model contain only  the right answers of a  given student
class StudentAnswer(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='stage_answers')
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, null=True, blank=True,related_name='question_stage')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='+', null=True)
def __str__(self):
    return self.question.text

class LastStudentAnswer(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='stage_last_answers')
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, null=True, blank=True,related_name='last_question_stage')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='+', null=True)
    result = models.BooleanField()
    date = models.DateTimeField(auto_now_add=True , null=True)
    last_entr =   models.DateTimeField(auto_now=True, null=True)
def __str__(self):
    return self.question.text


class TakenQuiz(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='taken_quizzes')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='taken_quizzes')
    score = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)
    last_entr =   models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.quiz.name
class CompletedStage(models.Model):
        student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='completed_stages')
        stage = models.ForeignKey(Stage, on_delete=models.CASCADE, related_name='user_stages')
        score = models.FloatField()
        date = models.DateTimeField(auto_now_add=True)
        last_entr =   models.DateTimeField(auto_now=True)

class TakenBadge(models.Model):
     student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='taken_badges')
     badge = models.ForeignKey(Badge, on_delete=models.CASCADE, related_name='taken_badges', default='')
     date = models.DateTimeField(auto_now_add=True)
     score = models.FloatField()
