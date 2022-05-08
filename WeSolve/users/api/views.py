from queue import Empty
from requests import request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, mixins, viewsets
from rest_framework import permissions
from users.models import CustomUser, Faculty, School, Course
from users.api.serializers import (UserDisplaySerializer, 
                                   UserAdminDisplaySerializer,
                                   FacultyListSerializer,
                                   SchoolListSerializer,
                                   CourseListSerializer)
from users.api.renderers import myRenderer


class FacultyListAPIView(generics.ListAPIView):
    queryset = Faculty.objects.all()
    serializer_class = FacultyListSerializer


class SchoolListAPIView(generics.ListAPIView):
    serializer_class = SchoolListSerializer
    # queryset = School.objects.all()
    renderer_classes = [myRenderer]

    def get_queryset(self):
        queryset = School.objects.all()
        faculty = self.request.query_params.get("faculty")
        assert faculty is not None , (
            'faculty argument missing'
        )
        if faculty is not None:
            queryset = queryset.filter(facultyName=faculty)
        assert queryset , (
            '"%s" faculty dosent have any schools in our website' % faculty
        )
        return queryset
    
    # def get(self, request, *args, **kwargs):
    #     faculty = self.request.query_params.get("faculty")
    #     print(faculty)
    #     return super().get(request, *args, **kwargs)
    

class CourseListAPIView(generics.ListAPIView):
    serializer_class = CourseListSerializer

    def get_queryset(self):
        queryset = Course.objects.all()
        school = self.request.query_params.get("school")
        assert school is not None , (
            'school argument missing'
        )
        if school is not None:
            queryset = queryset.filter(schoolName=school)
        assert queryset , (
            '"%s" school dosent have any courses in our website' % school
        )
        return queryset



class UserListAPIView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserAdminDisplaySerializer
    permission_classes = [permissions.IsAdminUser]

# class CurrentUserAPIView(generics.RetrieveUpdateDestroyAPIView):
#     qureyset = CustomUser.objects.all()
#     serializer_class = UserDisplaySerializer

class CurrentUserAPIView(mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin,
                         viewsets.GenericViewSet):
    
    permission_class = [permissions.IsAuthenticated]
    serializer_class = UserDisplaySerializer

    def get_object(self):
        return self.request.user

# class CurrentUserAPIView(APIView):

#     def get(self, request):
#         serializer = UserDisplaySerializer(request.user)
#         return Response(serializer.data)
    
