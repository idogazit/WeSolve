from rest_framework import serializers
from users.forms import NewUserForm


class UserDisplaySerializer(serializers.ModelSerializer):

    class Meta:
        model = NewUserForm
        fields = ["username"]