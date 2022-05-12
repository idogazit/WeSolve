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

    path("answers/<str:answerId>/", 
         qv.AnswerRUDAPIView.as_view(),
         name="answer-detail"),

    path("answers/<str:answerId>/upvote/", 
         qv.AnswerUpvoteAPIView.as_view(),
         name="answer-upvote"),
     
     path("answers/<str:answerId>/downvote/", 
          qv.AnswerDownvoteAPIView.as_view(),
          name="answer-downvote"),
     
     path("nav/<str:course>/exams/", 
          qv.examAPIView.as_view(),
          name="exam-list"),
     
     path("nav/<str:exam>/questions/",
          qv.QuestionListAPIView.as_view(),
          name="exam-questions-list")
]