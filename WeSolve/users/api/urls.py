from django.urls import path
from users.api.views import (CurrentUserAPIView, 
                             UserListAPIView,
                             FacultyListAPIView,
                             SchoolListAPIView)


urlpatterns = [
    path("users/", UserListAPIView.as_view(), name="user-list"),
    path("users/current/", 
        CurrentUserAPIView.as_view({'get' : 'retrieve', 
                                    'post' : 'update', 
                                    'delete' : 'destroy'}), 
        name="current-user"),
    path("nav/faculties/", FacultyListAPIView.as_view(), name="faculty-list"),
    path("nav/schools/", SchoolListAPIView.as_view(), name="school-list")

]