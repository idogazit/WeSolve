from requests import request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, mixins, viewsets
from rest_framework import permissions
from users.models import CustomUser
from users.api.serializers import UserDisplaySerializer, UserAdminDisplaySerializer


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
    
