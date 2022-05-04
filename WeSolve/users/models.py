import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class Course(models.Model):
    courseId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    courseName = models.CharField(max_length=50, unique=True)
    courseNumber = models.CharField(max_length=50, unique=True)
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

    def __str__(self):
        return self.username

    

