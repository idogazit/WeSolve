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
                                       QuestionTopicListSerializer,
                                       QuestionLabelSerializer)
from questions.models import Answer, Question, Exam, QuestionLabel, Label, QuestionTopic
from questions.api.renderers import examRenderer
import uuid
from django.db.models import Count
from users.models import CustomUser
from users.models import Topic

from itertools import chain


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

        if user in answer.downvoters:
            answer.downvoters.remove(user)
            answer.ranking += 1
        
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

        if user in answer.upvoters:
            answer.upvoters.remove(user)
            answer.ranking -= 1
        
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


class QuestionLabelListAPIView(generics.ListCreateAPIView):
    serializer_class = QuestionLabelSerializer
    output_label_user = CustomUser.objects.get(username="admin")

    def get_queryset(self):
        kwarg_question = self.kwargs.get("question")
        queryset = QuestionLabel.objects.filter(questionId=kwarg_question)
        diff_query = queryset.filter(labelName='Difficulty')
        type_query = queryset.filter(labelName='Question Type')
        precent_query = queryset.filter(labelName='Points Percentage')
        importance_query = queryset.filter(labelName='Importance')

        diff_label = self.getAverageNumericLabel(diff_query)
        type_label = self.getMaxOccurenceLabel(type_query)
        precent_label = self.getMaxOccurenceLabel(precent_query)
        importance_label = self.getAverageNumericLabel(importance_query)

        label_list = []

        if diff_label:
            label_list.append(diff_label)
        if type_label:
            label_list.append(type_label)
        if precent_label:
            label_list.append(precent_label)
        if importance_label:
            label_list.append(importance_label)
        
        none_qs = QuestionLabel.objects.none()
        qs = list(chain(none_qs, label_list))


        return qs
    
    def getAverageNumericLabel(self, queryset):
        avg = 0
        count = len(queryset)
        if count == 0:
            return None # may need to change
        for user_rank in queryset:
            avg += int(user_rank.labelValue)
        avg = avg / count
        avg = "{:.2f}".format(avg)
        ans = QuestionLabel(questionId=queryset[0].questionId,
                            labeledByUser=self.output_label_user,
                            labelName=queryset[0].labelName,
                            labelValue=str(avg))
        return ans
    
    def getMaxOccurenceLabel(self, queryset):
        labels = {}
        count = len(queryset)
        if count == 0:
            return None # may need to change
        for user_label in queryset:
            l = user_label.labelValue
            if l in labels:
                labels[l] += 1
            else:
                labels[l] = 1
        final_label = max(labels, key=labels.get)
        ans = QuestionLabel(questionId=queryset[0].questionId,
                            labeledByUser=self.output_label_user,
                            labelName=queryset[0].labelName,
                            labelValue=final_label)
        return ans
    
    def post(self, request, question):
        questionObject = get_object_or_404(Question, questionId=question)
        user = request.user
        label = get_object_or_404(Label, labelName=request.data.get('labelName'))
        if QuestionLabel.objects.filter(questionId=questionObject, labeledByUser=user, labelName=label).exists():
            # consider possibility of updating rating, maybe change to ListCreateUpdateAPIView
            raise ValidationError("You have already gave rating to this Question Label!")
        

        value = request.data.get('labelValue')
        if not label.possibleValues.filter(labelValue=value).exists():
            raise ValidationError("Given label value is not valid!")
        
        labelQuest = QuestionLabel.objects.create(questionId=questionObject,
                                                     labeledByUser=user, 
                                                     labelName=label, 
                                                     labelValue=value)

        serializer_context = {"request": request}
        serializer = self.serializer_class(labelQuest, context=serializer_context)
        return Response(serializer.data, status=status.HTTP_200_OK)


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