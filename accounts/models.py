from django.db import models
from django.contrib.auth.models import User
from colorful.fields import RGBColorField
from django.db.models.signals import post_save
from django.dispatch import receiver


#make the email field unique
User._meta.get_field('email')._unique = True



class Tag(models.Model):
    name = models.CharField(max_length=30)
    color = RGBColorField(max_length=7, default='#007bff')

    def __str__(self):
        return self.name



class Quiz(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='quiz_logo/',null=True,blank=True)
    tags = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='quizzes' )
    point = models.IntegerField(null=True, default=0)
    approved = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    def __str__(self):
        return self.name
    def get_quiz_tags(self):
        return str(list(self.tags.all().values_list('name', flat= True)))

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
    point = models.FloatField()
    logo = models.ImageField(upload_to='badge_logo/',null=True,blank=True)

class StudentLevel(models.Model):

    Novice  = 1
    Apprentice = 2   #120
    Trainee = 3      #50
    Beginner =  4    #34
    Amateur  = 5     #22
    Professional  = 6#17
    Master = 7       #13
    Wizard =8        # 9
    Mage = 9         # 7
    White_Mage = 10  # 5
    Regent = 11      #3
    King = 12        # 1

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
    graduation_number = models.IntegerField(null=True, blank = True)
    exp_required = models.  PositiveIntegerField(null=True, blank = True)


    def __str__(self):
        return self.get_name_display()

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='student')
     #is_conf = model.BooleanField(default=False)
    bio = models.TextField(null=True, max_length = 500)
    photo = models.ImageField(upload_to='picture_profile/',default='default-96.png',blank=True)
    quizzes = models.ManyToManyField(Quiz, blank = True, through='TakenQuiz' ,related_name='quize_student')
    interests = models.ManyToManyField(Tag,blank=True, related_name='interested_students')
    exp = models.PositiveIntegerField(db_index=True,blank=True,default=1)
    rank = models.ForeignKey(StudentLevel ,on_delete=models.CASCADE,default=1 , related_name='level')
    level = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.user.username

    def calculate_level(self):
        import math
        level = int(1/4 * math.sqrt(self.exp))+1

        self.level = level
        self.save()
        return level
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Student.objects.create(user=instance)
    def get_student_interests(self):
        return str(list(self.interests.all().values_list('name', flat=True)))

def calculate_rank():

    users_ranks = StudentLevel.objects.all().order_by('exp_required')
    for rank in users_ranks:
        #go down to the previous rank
        if rank.name > 1:
            students = Student.objects.filter(rank = rank)
            print("all students of " + str(rank))
            print(students)
            if students.count() > rank.graduation_number :

                 student = students.order_by('exp').first()
                 print("last student studentin : "+str(student.rank))
                 print(student)
                 previous_rank =  StudentLevel.objects.filter(name__lt = rank.name).last()
                 Student.objects.filter(user = student.user).update(rank = previous_rank)
        #go to the next rank
        if rank.name < 12:
         student = Student.objects.filter(rank = rank).order_by('-exp').first()
         if student is not None:
            if student.exp > rank.exp_required:
                next_rank = StudentLevel.objects.filter(name__gt = rank.name).first()
                students = Student.objects.filter(rank = next_rank)
                if students.count()  <= next_rank.graduation_number:
                    Student.objects.filter(user = student.user).update(rank = next_rank)








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
        date = models.DateTimeField(auto_now=True)
        last_entr =   models.DateTimeField(auto_now_add=True)
        def __str__(self):
            return self.stage.name

class TakenBadge(models.Model):
     student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='taken_badges')
     badge = models.ForeignKey(Badge, on_delete=models.CASCADE, related_name='taken_badges', default='')
     date = models.DateTimeField(auto_now_add=True)
