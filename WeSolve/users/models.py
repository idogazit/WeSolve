import uuid
from django.db import models

# Create your models here.

class Course(models.Model):

    courseId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    courseName = models.CharField(max_length=50, unique=True)
    courseNumber = models.CharField(max_length=50, unique=True)
    # participants attribute is ManyToManyField relation to Users

    def __str__(self):
        return f'{self.courseNumber}_{self.courseName}'

    class Meta:
        db_table = 'Courses'


class User(models.Model):
    
    """
    Contains only users data for site's features.
    Users data for authentication is saved under Django's default Users table, for example:
    username (same as here), first_name, last_name, email, password (hash only), date_joined
    """ 
    class Rank(models.IntegerChoices):
        FRESHMAN = 0
        JUNIOR = 1
        SENIOR = 2

    def upload_location(self, filename):
        suffix = (filename.split('.'))[len(filename.split('.')) - 1]
        return f'website/uploads/userPics/{self.username}_userPic.{suffix}'

    userId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=30, unique=True) # same as the username in the users authentication table
    courses = models.ManyToManyField(Course, related_name='participants', blank=True) # userCourses relation
    rank = models.IntegerField(choices=Rank.choices, default=Rank.FRESHMAN)
    userPic = models.ImageField(upload_to=upload_location, default="website/uploads/userPics/default_userPic.png")
    isTeacher = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'Users'


