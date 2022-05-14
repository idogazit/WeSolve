from rest_framework import generics, status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from questions.api.permissions import IsAuthorOrReadOnly
from questions.api.serializers import (AnswerSerializer,
                                       QuestionSerializer, 
                                       ExamSerializer, 
                                       LabelListSerializer,
                                       QuestionLabelListSerializer,
                                       QuestionTopicListSerializer)
from questions.models import Answer, Question, Exam, QuestionLabel, Label, QuestionTopic
from questions.api.renderers import examRenderer

from django.db.models import Count

from users.models import Topic

class AnswerCreateAPIView(generics.CreateAPIView):
    """Allow users to answer a question instance if they haven't already."""
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        request_user = self.request.user
        kwarg_slug = self.kwargs.get("slug")
        question = get_object_or_404(Question, slug=kwarg_slug)

        if question.answers.filter(author=request_user).exists():
            raise ValidationError("You have already answered this Question!")

        serializer.save(author=request_user, question=question)


class AnswerUpvoteAPIView(APIView):
    """Allow users to add/remove a upvotes to/from an answer instance."""
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "answerId"

    def delete(self, request, pk):
        """Remove request.user from the upvoters queryset of an answer instance."""
        answer = get_object_or_404(Answer, pk=pk)
        user = request.user

        answer.upvoters.remove(user)
        answer.ranking -= 1
        answer.save()

        serializer_context = {"request": request}
        serializer = self.serializer_class(answer, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        """Add request.user to the upvoters queryset of an answer instance."""
        answer = get_object_or_404(Answer, pk=pk)
        user = request.user

        answer.upvoters.add(user)
        answer.ranking += 1
        answer.save()

        serializer_context = {"request": request}
        serializer = self.serializer_class(answer, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)


class AnswerDownvoteAPIView(APIView):
    """Allow users to add/remove a downvote to/from an answer instance."""
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "answerId"

    def delete(self, request, pk):
        """Remove request.user from the downvoters queryset of an answer instance."""
        answer = get_object_or_404(Answer, pk=pk)
        user = request.user

        answer.downvoters.remove(user)
        answer.ranking += 1
        answer.save()

        serializer_context = {"request": request}
        serializer = self.serializer_class(answer, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        """Add request.user to the downvoters queryset of an answer instance."""
        answer = get_object_or_404(Answer, pk=pk)
        user = request.user

        answer.downvoters.add(user)
        answer.ranking -= 1
        answer.save()

        serializer_context = {"request": request}
        serializer = self.serializer_class(answer, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)


class AnswerListAPIView(generics.ListAPIView):
    """Provide the answers queryset of a specific question instance."""
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        kwarg_slug = self.kwargs.get("slug")
        return Answer.objects.filter(question__slug=kwarg_slug).order_by("-ranking")


class AnswerRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Provide *RUD functionality for an answer instance to it's author."""
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    lookup_field = "answerId"



class QuestionViewSet(viewsets.ModelViewSet):
    """Provide CRUD +L functionality for Question."""
    queryset = Question.objects.all().order_by("-created_at")
    lookup_field = "slug"
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class QuestionListAPIView(generics.ListAPIView):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        kwarg_exam = self.kwargs.get("exam")
        return Question.objects.filter(examUniqueName=kwarg_exam)


class QuestionLabelListAPIVIew(generics.ListCreateAPIView):
    serializer_class = QuestionLabelListSerializer

    def get_queryset(self):
        kwarg_question = self.kwargs.get("question")
        return QuestionLabel.objects.filter(questionId=kwarg_question)


class examAPIView(generics.ListAPIView):
    serializer_class = ExamSerializer
    renderer_classes = [examRenderer]

    def get_queryset(self):
        kwarg_course = self.kwargs.get("course")
        return Exam.objects.filter(courseName=kwarg_course)


class LabelListAPIView(generics.ListAPIView):
    """Provide the labels queryset"""
    serializer_class = LabelListSerializer
    permission_classes = [IsAuthenticated]
    queryset = Label.objects.all()


class QuestionTopicAPIView(generics.ListCreateAPIView):
    """
    Concrete view for listing a topicQuestions or creating a topicQuestion instance.
    """
    serializer_class = QuestionTopicListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """List all given topics records for a question"""
        kwarg_question = self.kwargs.get("questionId")
        return QuestionTopic.objects.filter(questionId=kwarg_question)
    

    """
    def get_queryset(self):
        ...
        topicsGiven = QuestionTopic.objects.filter(questionId=self.kwargs.get("questionId"))
        aggregated_topics = topicsGiven.all().values('topicName').annotate(total=Count('topicName')).order_by('total')
        return aggregated_topics.filter(total__gte=1)[:3]
    """  

    def post(self, request, questionId):
        """Add the request.user's given topic for a question.
          Create atopicQuestions instance."""
        user = request.user
        question = get_object_or_404(Question, questionId=questionId)
        topic = get_object_or_404(Topic, topicName=request.data.get('topicName'))

        if QuestionTopic.objects.filter(questionId=question, labeledByUser=user, topicName=topic).exists():
            raise ValidationError("You have already gave this topic to this Question!")

        topicQuest = QuestionTopic.objects.create(questionId=question, labeledByUser=user, topicName=topic)

        serializer_context = {"request": request}
        serializer = self.serializer_class(topicQuest, context=serializer_context)
        return Response(serializer.data, status=status.HTTP_200_OK)