from django.urls import path
from users.api.views import CurrentUserAPIView, UserListAPIView


urlpatterns = [
    path("users/", UserListAPIView.as_view(), name="user-list"),
    path("users/current/", CurrentUserAPIView.as_view({'get' : 'retrieve', 'post' : 'update', 'delete' : 'destroy'}), name="current-user")
]