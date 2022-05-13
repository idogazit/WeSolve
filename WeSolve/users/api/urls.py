from django.urls import path
from users.api.views import (CurrentUserAPIView, 
                             UserListAPIView,
                             FacultyListAPIView,
                             SchoolListAPIView,
                             CourseListAPIView,
                             TopicListAPIView)


urlpatterns = [
    path("users/", UserListAPIView.as_view(), name="user-list"),
    path("users/current/", 
        CurrentUserAPIView.as_view({'get' : 'retrieve', 
                                    'post' : 'update', 
                                    'delete' : 'destroy'}), 
        name="current-user"),
    path("nav/faculties/", FacultyListAPIView.as_view(), name="faculty-list"),
    path("nav/<str:faculty>/schools/", SchoolListAPIView.as_view(), name="school-list"),
    path("nav/<str:school>/courses/", CourseListAPIView.as_view(), name="course-list"),
    path("topics/", TopicListAPIView.as_view(), name="topic-list")
]