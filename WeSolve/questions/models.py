import uuid
import users.models as usersModels
from django.db import models

# Create your models here.


class Exam(models.Model):
    examId = models.UUIDField(primary_key=True, default=uuid.uuid4,  editable=False)
    courseName = models.ForeignKey(usersModels.Course, on_delete=models.DO_NOTHING, to_field='courseName')
    teacher = models.ForeignKey(usersModels.User, on_delete=models.DO_NOTHING, to_field='username', limit_choices_to={'isTeacher': True}) 
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
        return f'website/uploads/questionsPics/{self.questionId}_questionPic.{suffix}'

    questionId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    examId = models.ForeignKey(Exam, on_delete=models.DO_NOTHING, to_field='examId')
    questionPic = models.ImageField(upload_to=upload_location, blank=True)

    def __str__(self):
        return str(self.questionId)

    class Meta:
        db_table = 'Questions'


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
    labeledByUser = models.ForeignKey(usersModels.User, on_delete=models.DO_NOTHING, to_field='username')
    labelName = models.ForeignKey(Label, on_delete=models.DO_NOTHING, to_field='labelName')
    labelValue = models.CharField(max_length=50) # make sure is a possible value!!!

    def __str__(self):
        return str(self.questionLabelId)

    class Meta:
        db_table = 'QuestionLabels'


class Solution(models.Model):

    def upload_location(self, filename):
        suffix = (filename.split('.'))[len(filename.split('.')) - 1]
        return f'website/uploads/solutionsPics/{self.solutionId}_solutionPic.{suffix}'

    solutionId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    questionId = models.ForeignKey(Question, on_delete=models.DO_NOTHING, to_field='questionId')
    uploadedByUser = models.ForeignKey(usersModels.User, on_delete=models.DO_NOTHING, to_field='username')
    solutionPic = models.ImageField(upload_to=upload_location)

    def __str__(self):
        return str(self.solutionId)

    class Meta:
        db_table = 'Solutions'


class SolutionRanking(models.Model):
    solutionRankingId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    solutionId = models.ForeignKey(Solution, on_delete=models.DO_NOTHING, to_field='solutionId')
    rankedByUser = models.ForeignKey(usersModels.User, on_delete=models.DO_NOTHING, to_field='username')
    rankingValue = models.CharField(max_length=10, choices=[('up', 'Upvote'), ('down', 'Downvote')], default=('up', 'Upvote'))

    def __str__(self):
        return str(self.solutionRankingId)

    class Meta:
        db_table = 'SolutionRankings'
