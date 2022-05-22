import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class Faculty(models.Model):
    facultyId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    facultyName = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f'{self.facultyName}'

    class Meta:
        db_table = 'Faculties'


class School(models.Model):
    schoolId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    schoolName = models.CharField(max_length=50, unique=True)
    facultyName = models.ForeignKey(Faculty, default='Exact Sciences', on_delete=models.CASCADE, to_field='facultyName')

    def __str__(self):
        return f'{self.schoolName}'

    class Meta:
        db_table = 'Schools'


class Topic(models.Model):
    topicId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    topicName = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f'{self.topicName}'

    class Meta:
        db_table = 'Topics'


class Course(models.Model):
    courseId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    courseName = models.CharField(max_length=50, unique=True)
    courseNumber = models.CharField(max_length=50, unique=True)
    schoolName = models.ForeignKey(School, default='Computer Science', on_delete=models.CASCADE, to_field='schoolName')
    topics = models.ManyToManyField(Topic, blank=True)
    # participants attribute is ManyToManyField relation to Users

    def __str__(self):
        return f'{self.courseNumber}_{self.courseName}'

    class Meta:
        db_table = 'Courses'


class CustomUser(AbstractUser):
    """
    Extends AbstractUser with users data for site's features.
    Users data for authentication is saved under Django's default Users table:
    username (same as here), first_name, last_name, email, password (hash only), date_joined
    """ 
    class Rank(models.IntegerChoices):
        FRESHMAN = 0
        JUNIOR = 1
        SENIOR = 2

    def upload_location(self, filename):
        suffix = (filename.split('.'))[len(filename.split('.')) - 1]
        return f'users/uploads/userPics/{self.username}_userPic.{suffix}'

    userId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    courses = models.ManyToManyField(Course, related_name='participants', blank=True) # userCourses relation
    rank = models.IntegerField(choices=Rank.choices, default=Rank.FRESHMAN)
    userPic = models.ImageField(upload_to=upload_location, default="users/uploads/userPics/default_userPic.png")
    isTeacher = models.BooleanField(default=False)
    rankScore = models.IntegerField(default=0, blank=False)

    def __str__(self):
        return self.username

    

