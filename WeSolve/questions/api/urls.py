from django.urls import include, path
from rest_framework.routers import DefaultRouter

from questions.api import views as qv

router = DefaultRouter()
router.register(r"questions", qv.QuestionViewSet)

urlpatterns = [
    path("", include(router.urls)), 

    path("questions/<slug:slug>/answers/", 
         qv.AnswerListAPIView.as_view(),
         name="answer-list"),

    path("questions/<slug:slug>/answer/", 
         qv.AnswerCreateAPIView.as_view(),
         name="answer-create"),

    path("answers/<int:pk>/", 
         qv.AnswerRUDAPIView.as_view(),
         name="answer-detail"),

    path("answers/<int:pk>/like/", 
         qv.AnswerLikeAPIView.as_view(),
         name="answer-like"),
     
     path("nav/<str:course>/exams/", 
          qv.examAPIView.as_view(),
          name="exam-list"),
     
     path("nav/<str:exam>/questions/",
          qv.QuestionListAPIView.as_view(),
          name="exam-questions-list"),

     path("labels/",
          qv.LabelListAPIView.as_view(),
          name="labels-list"),

     path("questions/<str:questionId>/topics/",
          qv.QuestionTopicAPIView.as_view(),
          name="topics-get-create")
]