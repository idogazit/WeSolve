import uuid
from django.db import models
from django.conf import settings
import users.models as usersModels
from django.core.validators import FileExtensionValidator


class Exam(models.Model):
    examId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    courseName = models.ForeignKey(usersModels.Course, on_delete=models.CASCADE, to_field='courseName')
    year = models.IntegerField(default=2022)
    semester = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B')], default=('A', 'A'))
    examType = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B')], default=('A', 'A')) # moed A or B

    def __str__(self):
        return f'{self.courseName}_{self.year}_{self.semester}_{self.examType}'

    class Meta:
        db_table = 'Exams'


class Question(models.Model):

    def upload_location(self, filename):
        return f'questions/uploads/questionsPDF/{self.questionId}_question.pdf'

    questionId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    examUniqueName = models.ForeignKey(Exam, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="questions", default='cdf09df6-6e9e-42b0-928b-b119ce4f86bb', limit_choices_to={'isTeacher': True})
    content = models.CharField(max_length=240, default='') # Question number
    questionPDF = models.FileField(upload_to=upload_location, default='', validators=[FileExtensionValidator(['pdf'])])
    slug = models.SlugField(max_length=255, default='', blank=True)
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
    questionId = models.ForeignKey(Question, on_delete=models.CASCADE, to_field='questionId')
    labeledByUser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, to_field='username')
    labelName = models.ForeignKey(Label, on_delete=models.CASCADE, to_field='labelName')
    labelValue = models.CharField(max_length=50) # make sure is a possible value!!!

    def __str__(self):
        return str(self.questionLabelId)

    class Meta:
        db_table = 'QuestionLabels'


class QuestionTopic(models.Model):
    questionTopicId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    questionId = models.ForeignKey(Question, on_delete=models.CASCADE, to_field='questionId')
    labeledByUser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, to_field='username')
    topicName = models.ForeignKey(usersModels.Topic, on_delete=models.CASCADE, to_field='topicName')

    def __str__(self):
        return str(self.questionTopicId)

    class Meta:
        db_table = 'QuestionTopics'


class Answer(models.Model):

    def upload_location(self, filename):
        return f'questions/uploads/answersPDF/{self.answerId}_answer.pdf'

    answerId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers", to_field='questionId')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, to_field='username')
    body = models.TextField(default='', blank=True)
    answerPDF = models.FileField(upload_to=upload_location, default='', blank=True, validators=[FileExtensionValidator(['pdf'])])
    downvoters = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="downvotes", blank=True)
    upvoters = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="upvotes", blank=True)
    ranking = models.IntegerField(blank=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.answerId)


