from re import M
from rest_framework import generics, status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
# from rest_framework.parsers import MultiPartParser, FileUploadParser

from questions.api.permissions import IsAuthorOrReadOnly
from questions.api.serializers import (AnswerSerializer,
                                       QuestionSerializer, 
                                       ExamSerializer, 
                                       LabelListSerializer,
                                       QuestionTopicListSerializer,
                                       QuestionLabelSerializer,
                                       BreadcrumbsSerializer)
from questions.models import Answer, Question, Exam, QuestionLabel, Label, QuestionTopic
from questions.api.renderers import examRenderer, crumbsRenderer
from users.models import CustomUser
from users.models import Topic

from itertools import chain
from collections import Counter


SELF_VOTE_SCORE = 1
UPVOTE_SCORE = 2
DOWNVOTE_SCORE = -2
ANSWER_SCORE = 10
ADDED_LABEL_SCORE = 3
ADDED_TOPIC_SCORE = 3
SPAMMER_SCORE = -100


class AnswerCreateAPIView(generics.CreateAPIView):
    """Allow users to answer a question instance if they haven't already."""
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]


    def perform_create(self, serializer):
        request_user = self.request.user
        kwarg_slug = self.kwargs.get("slug")
        question = get_object_or_404(Question, slug=kwarg_slug)

        if self.request.user.rankScore < SPAMMER_SCORE:
            raise ValidationError("Your rank score is too low to perform this action!")

        if question.answers.filter(author=request_user).exists():
            raise ValidationError("You have already answered this Question!")
        
        request_user.rankScore += ANSWER_SCORE
        set_user_rank(request_user)
        request_user.save()
        
        serializer.save(author=request_user, question=question)
    

def set_user_rank(user):
    if user.rankScore >= 300:
        user.rank = CustomUser.Rank.SENIOR
    elif user.rankScore >= 100:
        user.rank = CustomUser.Rank.JUNIOR
    else:
        user.rank = CustomUser.Rank.FRESHMAN

        

class AnswerUpvoteAPIView(APIView):
    """Allow users to add/remove a upvotes to/from an answer instance."""
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "answerId"

    def delete(self, request, answerId):
        """Remove request.user from the upvoters queryset of an answer instance."""
        answer = get_object_or_404(Answer, answerId=answerId)
        user = request.user
        author = answer.author

        if self.request.user.rankScore < SPAMMER_SCORE:
            raise ValidationError("Your rank score is too low to perform this action!")

        answer.upvoters.remove(user)
        user.rankScore -= SELF_VOTE_SCORE
        author.rankScore -= UPVOTE_SCORE
        set_user_rank(user)
        set_user_rank(author)
        answer.ranking -= 1
        user.save()
        author.save()
        answer.save()

        serializer_context = {"request": request}
        serializer = self.serializer_class(answer, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, answerId):
        """Add request.user to the upvoters queryset of an answer instance."""
        answer = get_object_or_404(Answer, answerId=answerId)
        user = request.user
        author = answer.author

        if self.request.user.rankScore < SPAMMER_SCORE:
            raise ValidationError("Your rank score is too low to perform this action!")

        if user in answer.downvoters.all():
            answer.downvoters.remove(user)
            answer.ranking += 1
            user.rankScore -= SELF_VOTE_SCORE
            author.rankScore -= DOWNVOTE_SCORE
        
        answer.upvoters.add(user)
        answer.ranking += 1
        user.rankScore += SELF_VOTE_SCORE
        author.rankScore += UPVOTE_SCORE
        set_user_rank(user)
        set_user_rank(author)
        answer.save()
        user.save()
        author.save()

        serializer_context = {"request": request}
        serializer = self.serializer_class(answer, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)


class AnswerDownvoteAPIView(APIView):
    """Allow users to add/remove a downvote to/from an answer instance."""
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "answerId"

    def delete(self, request, answerId):
        """Remove request.user from the downvoters queryset of an answer instance."""
        answer = get_object_or_404(Answer, answerId=answerId)
        user = request.user
        author = answer.author

        if self.request.user.rankScore < SPAMMER_SCORE:
            raise ValidationError("Your rank score is too low to perform this action!")

        answer.downvoters.remove(user)
        user.rankScore -= SELF_VOTE_SCORE
        author.rankScore -= DOWNVOTE_SCORE
        set_user_rank(user)
        set_user_rank(author)
        answer.ranking += 1
        user.save()
        author.save()
        answer.save()

        serializer_context = {"request": request}
        serializer = self.serializer_class(answer, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, answerId):
        """Add request.user to the downvoters queryset of an answer instance."""
        answer = get_object_or_404(Answer, answerId=answerId)
        user = request.user
        author = answer.author

        if self.request.user.rankScore < SPAMMER_SCORE:
            raise ValidationError("Your rank score is too low to perform this action!")

        if user in answer.upvoters.all():
            answer.upvoters.remove(user)
            answer.ranking -= 1
            user.rankScore -= SELF_VOTE_SCORE
            author.rankScore -= UPVOTE_SCORE

        
        answer.downvoters.add(user)
        answer.ranking -= 1
        user.rankScore += SELF_VOTE_SCORE
        author.rankScore += DOWNVOTE_SCORE
        set_user_rank(user)
        set_user_rank(author)
        answer.save()
        user.save()
        author.save()

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

def get_labelset(kwarg_question):
    output_label_user = CustomUser.objects.get(username="admin")
    queryset = QuestionLabel.objects.filter(questionId=kwarg_question)
    diff_query = queryset.filter(labelName='Difficulty')
    type_query = queryset.filter(labelName='Question Type')
    precent_query = queryset.filter(labelName='Points Percentage')
    importance_query = queryset.filter(labelName='Importance')

    diff_label = getAverageNumericLabel(diff_query, output_label_user)
    type_label = getMaxOccurenceLabel(type_query, output_label_user)
    precent_label = getMaxOccurenceLabel(precent_query, output_label_user)
    importance_label = getAverageNumericLabel(importance_query, output_label_user)

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

def getAverageNumericLabel(queryset, output_label_user):
    avg = 0
    count = queryset.count()
    if count == 0:
        return None # may need to change
    for user_rank in queryset:
        avg += int(user_rank.labelValue)
    avg = avg / count
    avg = "{:.2f}".format(avg)
    ans = QuestionLabel(questionId=queryset[0].questionId,
                        labeledByUser=output_label_user,
                        labelName=queryset[0].labelName,
                        labelValue=str(avg))
    return ans

def getMaxOccurenceLabel(queryset, output_label_user):
    labels = {}
    count = queryset.count()
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
                        labeledByUser=output_label_user,
                        labelName=queryset[0].labelName,
                        labelValue=final_label)
    return ans



class QuestionLabelListAPIView(generics.ListCreateAPIView):
    serializer_class = QuestionLabelSerializer
    output_label_user = CustomUser.objects.get(username="admin")
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        kwarg_question = self.kwargs.get("question")
        return get_labelset(kwarg_question)
    
    def post(self, request, question):
        questionObject = get_object_or_404(Question, questionId=question)
        user = request.user
        label = get_object_or_404(Label, labelName=request.data.get('labelName'))

        if self.request.user.rankScore < SPAMMER_SCORE:
            raise ValidationError("Your rank score is too low to perform this action!")

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
        
        user.rankScore += ADDED_LABEL_SCORE
        set_user_rank(user)
        user.save()

        serializer_context = {"request": request}
        serializer = self.serializer_class(labelQuest, context=serializer_context)
        return Response(serializer.data, status=status.HTTP_200_OK)


class examAPIView(generics.ListAPIView):
    serializer_class = ExamSerializer
    renderer_classes = [examRenderer]

    def get_queryset(self):
        kwarg_course = self.kwargs.get("course")
        return Exam.objects.filter(courseName=kwarg_course).defer("courseName")


class LabelListAPIView(generics.ListAPIView):
    """Provide the labels queryset"""
    serializer_class = LabelListSerializer
    permission_classes = [IsAuthenticated]
    queryset = Label.objects.all()


def get_topicset(kwarg_question):
    """List all given topics records for a question"""
    queryset = QuestionTopic.objects.filter(questionId=kwarg_question)
    output_label_user = CustomUser.objects.get(username="admin")
    new_queryset = getThreeMaxOccurenceTopics(queryset, output_label_user)
    none_qs = QuestionTopic.objects.none()
    if new_queryset:   
        qs = list(chain(none_qs, new_queryset))
        return qs
    return none_qs

def getThreeMaxOccurenceTopics(queryset, output_label_user):
    labels = {}
    count = len(queryset)
    if count == 0:
        return None # may need to change
    for user_topic in queryset:
        l = user_topic.topicName
        if l in labels:
            labels[l] += 1
        else:
            labels[l] = 1
    final_topics = [k for k,v in Counter(labels).most_common(3)]
    new_queryset = []
    for topic in final_topics:
        ans = QuestionTopic(questionId=queryset[0].questionId,
                            labeledByUser=output_label_user,
                            topicName=topic)
        new_queryset.append(ans)
    return new_queryset  

class QuestionTopicAPIView(generics.ListCreateAPIView):
    """
    Concrete view for listing a topicQuestions or creating a topicQuestion instance.
    """
    serializer_class = QuestionTopicListSerializer
    permission_classes = [IsAuthenticated]
    output_label_user = CustomUser.objects.get(username="admin")


    def get_queryset(self):
        """List all given topics records for a question"""
        kwarg_question = self.kwargs.get("questionId")
        return get_topicset(kwarg_question)

    
    def post(self, request, questionId):
        """Add the request.user's given topic for a question.
          Create atopicQuestions instance."""
          
        user = request.user
        question = get_object_or_404(Question, questionId=questionId)
        topicName = str.lower(request.data.get('topicName'))

        if self.request.user.rankScore < SPAMMER_SCORE:
            raise ValidationError("Your rank score is too low to perform this action!")

        if not Topic.objects.filter(topicName=topicName):
            Topic.objects.create(topicName=topicName)

        topic = get_object_or_404(Topic, topicName=topicName)

        if QuestionTopic.objects.filter(questionId=question, labeledByUser=user, topicName=topic).exists():
            raise ValidationError("You have already gave this topic to this Question!")

        topicQuest = QuestionTopic.objects.create(questionId=question, labeledByUser=user, topicName=topic)

        user.rankScore += ADDED_TOPIC_SCORE
        set_user_rank(user)
        user.save()

        serializer_context = {"request": request}
        serializer = self.serializer_class(topicQuest, context=serializer_context)
        return Response(serializer.data, status=status.HTTP_200_OK)

class SimilarQuestionsAPIView(generics.ListAPIView):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        kwarg_question = self.kwargs.get("question")
        base_labels = get_labelset(kwarg_question)
        base_topics = get_topicset(kwarg_question)

        questions = Question.objects.exclude(questionId=kwarg_question)\
                        .only("questionId", "slug")

        distances = {}
        for q in questions:
            d = compute_distance(q.questionId, base_labels, base_topics)
            distances[q.slug] = d

        # get top 3 results from dict
        similar_slugs = sorted(distances, key=distances.get, reverse=False)[:3]
        return Question.objects.filter(slug__in=similar_slugs)


def compute_label_distance(labels, other_labels):
    """computes distance between group of labels"""
    if not labels or not other_labels:
        return 400

    df_v, o_df_v, imp_v, o_imp_v, typ_v, o_typ_v, pnts_v, o_pnts_v \
            = ('', '', '', '', '', '', '', '')

    for l in labels:
        if l.labelName == "Difficulty":
            df_v = int(l.labelValue)
        elif l.labelName == "Importance":
            imp_v = int(l.labelValue)
        elif l.labelName == "Question Type":
            typ_v = l.labelValue
        elif l.labelName == "Points Precentage":
            pnts_v = l.labelValue

    for l in other_labels:
        if l.labelName == "Difficulty":
            o_df_v = int(l.labelValue)
        elif l.labelName == "Importance":
            o_imp_v = int(l.labelValue)
        elif l.labelName == "Question Type":
            o_typ_v = l.labelValue
        elif l.labelName == "Points Precentage":
            o_pnts_v = l.labelValue


    if df_v == '' or o_df_v == '':
        diff_d = 20
    else:
        diff_d = 2 * abs( int(df_v) - int(o_df_v) )

    if imp_v == '' or o_imp_v == '':
        imp_d = 20
    else:
        imp_d = 2 * abs( int(imp_v) - int(o_imp_v) )
    
    if typ_v == '' or o_typ_v == '':
        type_d = 10
    else:
        type_d = 0 if (typ_v == o_typ_v) else 5
    
    # todo: change this
    if pnts_v == '' or o_pnts_v == '':
        points_d = 10
    else:
        points_d = 0 if (pnts_v == o_pnts_v) else 5

    return diff_d + imp_d + type_d + points_d


def compute_topic_distance(topics, other_topics):
    if not topics:
        return 500
    topics_vals = [t.topicName for t in topics]
    o_topics_vals = [t.topicName for t in other_topics]

    n = len(set(topics_vals).intersection(o_topics_vals))
    m = len(set(topics_vals).union(set(o_topics_vals)))

    return (1 - n / m) * 10



def compute_distance(other_question, labels, topics):
    other_labels = get_labelset(other_question)
    other_topics = get_topicset(other_question)
    a = compute_label_distance(labels, other_labels)
    b = compute_topic_distance(topics, other_topics)
    return a + b



class breadCrumbsAPIView(generics.RetrieveAPIView):
    serializer_class = BreadcrumbsSerializer
    renderer_classes = [crumbsRenderer]
    lookup_field = "examId"
    queryset = Exam.objects.all()

