from rest_framework import serializers
from users.models import (CustomUser, Faculty, 
                            School, Course)


class UserDisplaySerializer(serializers.ModelSerializer):
    courses = serializers.StringRelatedField(many=True)

    class Meta:
        model = CustomUser
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "date_joined",
            "rank",
            "userPic",
            "isTeacher",
            "courses"
            ]

class UserAdminDisplaySerializer(serializers.ModelSerializer):
    courses = serializers.StringRelatedField(many=True)

    class Meta:
        model = CustomUser
        fields = "__all__"

class FacultyListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Faculty
        fields = "__all__"

class SchoolListSerializer(serializers.ModelSerializer):

    class Meta:
        model = School
        fields = "__all__"