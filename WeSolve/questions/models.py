import uuid
from django.db import models
from django.conf import settings
import users.models as usersModels


class Exam(models.Model):
    examId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    courseName = models.ForeignKey(usersModels.Course, on_delete=models.DO_NOTHING, to_field='courseName')
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, to_field='username', limit_choices_to={'isTeacher': True}) 
    year = models.IntegerField(default=2022)
    semester = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B')], default=('A', 'A'))
    examType = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B')], default=('A', 'A')) # moed A or B

    def __str__(self):
        return f'{self.courseName}_{self.year}_{self.semester}_{self.examType}'

    class Meta:
        db_table = 'Exams'


class Question(models.Model):

    def upload_location(self, filename):
        suffix = (filename.split('.'))[len(filename.split('.')) - 1]
        return f'questions/uploads/questionsPics/{self.questionId}_questionPic.{suffix}'

    questionId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    examId = models.ForeignKey(Exam, on_delete=models.DO_NOTHING, to_field='examId')
    questionPic = models.ImageField(upload_to=upload_location, default='')
    content = models.CharField(max_length=240, default='', blank=True)
    slug = models.SlugField(max_length=255, default='', blank=True)
    # author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name="questions")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.questionId)


class LabelValue(models.Model):
    labelValue = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.labelValue

    class Meta:
        db_table = 'LabelValues'


class Label(models.Model):
    labelId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    labelName = models.CharField(max_length=30, unique=True)
    possibleValues = models.ManyToManyField(LabelValue)

    def __str__(self):
        return self.labelName

    class Meta:
        db_table = 'Labels'


class QuestionLabel(models.Model):
    questionLabelId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    questionId = models.ForeignKey(Question, on_delete=models.DO_NOTHING, to_field='questionId')
    labeledByUser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, to_field='username')
    labelName = models.ForeignKey(Label, on_delete=models.DO_NOTHING, to_field='labelName')
    labelValue = models.CharField(max_length=50) # make sure is a possible value!!!

    def __str__(self):
        return str(self.questionLabelId)

    class Meta:
        db_table = 'QuestionLabels'


class Answer(models.Model):

    def upload_location(self, filename):
        suffix = (filename.split('.'))[len(filename.split('.')) - 1]
        return f'questions/uploads/answersPics/{self.answerId}_answerPic.{suffix}'

    answerId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.ForeignKey(Question, on_delete=models.DO_NOTHING, related_name="answers", to_field='questionId')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, to_field='username')
    answerPic = models.ImageField(upload_to=upload_location, default='')
    # body = models.TextField()
    downvoters = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="upvotes", blank=True)
    upvoters = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="downvotes", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.answerId)


