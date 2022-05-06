from rest_framework import serializers
from users.models import CustomUser


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

