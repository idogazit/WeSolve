from django.contrib import admin
from questions.models import Answer, Question, Exam, LabelValue, Label, QuestionLabel, QuestionTopic

class AnswerAdmin(admin.ModelAdmin):
    list_display = ["answerId", "question", "author", "body"]


class QuestionAdmin(admin.ModelAdmin):
    list_display = ["questionId", "examUniqueName", "author", "content"]

admin.site.register(Answer, AnswerAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Exam)
admin.site.register(LabelValue)
admin.site.register(Label)
admin.site.register(QuestionLabel)
admin.site.register(QuestionTopic)