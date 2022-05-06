from django.contrib import admin
from questions.models import Answer, Question, Exam, LabelValue, Label, QuestionLabel

admin.site.register(Answer)
admin.site.register(Question)
admin.site.register(Exam)
admin.site.register(LabelValue)
admin.site.register(Label)
admin.site.register(QuestionLabel)