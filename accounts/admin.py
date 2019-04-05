from django.contrib import admin
from .models import( Answer,Badge,Student,StudentAnswer,
Quiz,Question,TakenQuiz,TakenBadge,Tag, Stage, CompletedStage , LastStudentAnswer, StudentLevel
 , StageLevel)
"""

class YourModelAdmin(admin.ModelAdmin):

    form = YourModelForm

    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'extra_field',),
        }),
    )


"""
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['question', 'text']
    list_filter = ('question','text')

class QuestionAdmin(admin.ModelAdmin):
    list_display = ['stage', 'text', 'point']
    list_filter = ('stage','text')

class StudentAnswerAdmin(admin.ModelAdmin):
    list_display = ['student', 'stage', 'question']
    list_filter = ('student','stage')

class LastStudentAnswerAdmin(admin.ModelAdmin):
    list_display = ['student', 'stage', 'question', 'last_entr']
    list_filter = ('student','stage', 'result', 'last_entr',)

class TakenQuizAdmin(admin.ModelAdmin):
    list_display = ['student', 'quiz']
    list_filter = ('student','quiz')

class BadgeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    list_filter = ('name','description')

class StudentAdmin(admin.ModelAdmin):
    list_display = ['user', 'exp', 'rank']
    list_filter = ('rank','user')

class QuizAdmin(admin.ModelAdmin):
    list_display = ['name', 'tags']
    list_filter = ('name','tags')

class TakenQuizAdmin(admin.ModelAdmin):
    list_display = ['student', 'quiz']
    list_filter = ('student','quiz')

class TakenBadgeAdmin(admin.ModelAdmin):
    list_display = ['student', 'badge']
    list_filter = ('student','badge')

class StageAdmin(admin.ModelAdmin):
    list_display = ['name', 'quiz']
    list_filter = ('quiz',)
class CompletedStageAdmin(admin.ModelAdmin):
    list_display = ['student', 'stage']
    list_filter = ('student', 'stage')



admin.site.register(Badge, BadgeAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(StudentAnswer, StudentAnswerAdmin)
admin.site.register(LastStudentAnswer, LastStudentAnswerAdmin)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(TakenQuiz, TakenQuizAdmin)
admin.site.register(TakenBadge, TakenBadgeAdmin)
admin.site.register(Stage, StageAdmin)
admin.site.register(CompletedStage, CompletedStageAdmin)
admin.site.register(Tag)
admin.site.register(StudentLevel)
admin.site.register(StageLevel)
