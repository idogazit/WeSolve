from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Exam)
admin.site.register(LabelValue)
admin.site.register(Label)
admin.site.register(QuestionLabel)
admin.site.register(Question)
admin.site.register(Solution)
admin.site.register(SolutionRanking)