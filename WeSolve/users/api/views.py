from queue import Empty
from requests import request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, mixins, viewsets
from rest_framework import permissions
from users.models import CustomUser, Faculty, School, Course, Topic
from users.api.serializers import (UserDisplaySerializer, 
                                   UserAdminDisplaySerializer,
                                   FacultyListSerializer,
                                   SchoolListSerializer,
                                   CourseListSerializer,
                                   TopicListSerializer,)
from users.api.renderers import SchoolRenderer, CourseRenderer, facultyRenderer


class FacultyListAPIView(generics.ListAPIView):
    queryset = Faculty.objects.all()
    serializer_class = FacultyListSerializer
    renderer_classes = [facultyRenderer]


class SchoolListAPIView(generics.ListAPIView):
    serializer_class = SchoolListSerializer
    renderer_classes = [SchoolRenderer]

    def get_queryset(self):
        kwarg_faculty = self.kwargs.get("faculty")
        return School.objects.filter(facultyName=kwarg_faculty)
    
    

class CourseListAPIView(generics.ListAPIView):
    serializer_class = CourseListSerializer
    renderer_classes = [CourseRenderer]

    def get_queryset(self):
        kwarg_school = self.kwargs.get("school")
        return Course.objects.filter(schoolName=kwarg_school)



class UserListAPIView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserAdminDisplaySerializer
    permission_classes = [permissions.IsAdminUser]


class CurrentUserAPIView(mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin,
                         viewsets.GenericViewSet):
    
    permission_class = [permissions.IsAuthenticated]
    serializer_class = UserDisplaySerializer

    def get_object(self):
        return self.request.user


class TopicListAPIView(generics.ListAPIView):
    """Provide the topics queryset"""
    serializer_class = TopicListSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Topic.objects.all()
