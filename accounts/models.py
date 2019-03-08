from django.db import models
from django.contrib.auth.models import User
from colorful.fields import RGBColorField
#make the email field unique
User._meta.get_field('email')._unique = True



class Tag(models.Model):
    name = models.CharField(max_length=30)
    color = RGBColorField(max_length=7, default='#007bff')

    def __str__(self):
        return self.name
    def auto_generate_tag(self):
        return


class Quiz(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='quiz_logo/',null=True,blank=True)
    tags = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='quizzes' )
    point = models.IntegerField(null=True, default=0)
    approved = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    def __str__(self):
        return self.name

class StageLevel(models.Model):
    Beginner =1
    Easy = 2
    Normal = 3
    Hard = 4
    Very_hard = 5

    STATUS_CHOICES = (
        (Beginner , "beginner"),
        (Easy, "easy"),
        (Normal, "normal"),
        (Hard, "hard"),
        (Very_hard, "very hard"),
    )
    text = models.IntegerField(choices = STATUS_CHOICES, default=1)
    color = RGBColorField(max_length=7, default='#007bff')
    required_exp = models.PositiveIntegerField(db_index=True,blank=True,default=1)

    def __str__(self):
        return self.get_text_display()


class Stage(models.Model):
    name = models.CharField(max_length=255)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='stages')
    level = models.ForeignKey(StageLevel, blank=True , null=True, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    def __str__(self):
        return self.name

class Question(models.Model):
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, related_name='questiones')
    text = models.CharField('Question', null=True,blank=True,max_length=300)
    point = models.IntegerField(null=True, default=0)
    approved = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)

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
    logo = models.ImageField(upload_to='badge_logo/',null=True,blank=True)

class StudentLevel(models.Model):

    Novice  = 1
    Apprentice = 2
    Trainee = 3
    Beginner =  4
    Amateur  = 5
    Professional  = 6
    Master = 7
    Wizard =8
    Mage = 9
    White_Mage = 10
    Regent = 11
    King = 12

    STATUS_CHOICES =  (
        (Novice, "Novice"), (Apprentice, "Apprentice"), (Trainee, "Trainee"),
        (Beginner , "Beginner"), (Amateur , "Amateur "),  (Professional, "Professional"),
        (Master, "Master"),
        (Wizard , "Wizard "), (Mage, "Mage"), (White_Mage, "White Mage"),
        (Regent, "Regent"),  (King, "King"),
    )
    name = models.IntegerField(choices = STATUS_CHOICES, default=1 )
    logo = models.ImageField(upload_to='level_pic/',default=None,blank=True)
    description = models.TextField(max_length=200)

    def __str__(self):
        return self.get_name_display()

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='student')
     #is_conf = model.BooleanField(default=False)
    photo = models.ImageField(upload_to='picture_profile/',default='default-96.png',blank=True)
    quizzes = models.ManyToManyField(Quiz, blank = True, through='TakenQuiz' ,related_name='quize_student')
    interests = models.ManyToManyField(Tag,blank=True, related_name='interested_students')
    exp = models.PositiveIntegerField(db_index=True,blank=True,default=1)
    rank = models.ForeignKey(StudentLevel ,on_delete=models.CASCADE,blank=True, null=True , related_name='level')
    position = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.user.username

    def calculate_level(self):
        import math
        level = int(1/4 * math.sqrt(self.exp))
        return level
    def calculate_rank(self):
        all_ranks = StudentLevel.objects.all()
        #Novice
        if 0 <= self.exp <= 100:
            self.rank = all_ranks[0]
        #Apprentice
        if 101 <= self.exp <= 180:
            self.rank = all_ranks[1]
        #Trainee
        if  181 <= self.exp <= 300:
            self.rank = all_ranks[2]
        #Beginner
        if  301 <= self.exp <= 400:
            self.rank = all_ranks[3]
        #Amateur
        if  401 <= self.exp <= 500:
            self.rank = all_ranks[4]
        #Professional
        if  501 <= self.exp <= 600:
            self.rank = all_ranks[5]
        print(self.rank)
        return self.rank


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

    date = models.DateTimeField(auto_now_add=True)
    last_entr =   models.DateTimeField(auto_now=True)
    completed = models.BooleanField(null=True)
    def __str__(self):
        return self.quiz.name
class CompletedStage(models.Model):
        student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='completed_stages')
        quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True, related_name='stage_quizze')
        stage = models.ForeignKey(Stage, on_delete=models.CASCADE, related_name='user_stages')
        score = models.FloatField()
        date = models.DateTimeField(auto_now_add=True)
        last_entr =   models.DateTimeField(auto_now=True)
        def __str__(self):
            return self.stage.name

class TakenBadge(models.Model):
     student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='taken_badges')
     badge = models.ForeignKey(Badge, on_delete=models.CASCADE, related_name='taken_badges', default='')
     date = models.DateTimeField(auto_now_add=True)
     score = models.FloatField()
