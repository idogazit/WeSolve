from rest_framework import serializers
from questions.models import Answer, Question, Exam, Label, QuestionLabel, QuestionTopic
from users.models import Course, School



class AnswerSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    created_at = serializers.SerializerMethodField()
    upvotes_count = serializers.SerializerMethodField()
    downvotes_count = serializers.SerializerMethodField()
    user_has_upvoted = serializers.SerializerMethodField()
    user_has_downvoted = serializers.SerializerMethodField()
    question_slug = serializers.SerializerMethodField()
    is_teacher_approved = serializers.SerializerMethodField()

    class Meta:
        model = Answer
        exclude = ["question", "upvoters", "downvoters", "updated_at"]

    def get_created_at(self, instance):
        return instance.created_at.strftime("%B %d, %Y")

    def get_upvotes_count(self, instance):
        return instance.upvoters.count()
    
    def get_downvotes_count(self, instance):
        return instance.downvoters.count()
    
    def get_user_has_upvoted(self, instance):
        request = self.context.get("request")
        has_upvoted = instance.upvoters.filter(pk=request.user.pk).exists()
        return has_upvoted
    
    def get_user_has_downvoted(self, instance):
        request = self.context.get("request")
        has_downvoted = instance.downvoters.filter(pk=request.user.pk).exists()
        return has_downvoted

    def get_question_slug(self, instance):
        return instance.question.slug
    
    def get_is_teacher_approved(self, instance):
        return (instance.upvoters.filter(isTeacher=True).exists() or instance.author.isTeacher)


class QuestionSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    created_at = serializers.SerializerMethodField()
    slug = serializers.SlugField(read_only=True)
    answers_count = serializers.SerializerMethodField()
    user_has_answered = serializers.SerializerMethodField()

    class Meta:
        model = Question
        exclude = ["updated_at"]

    def get_created_at(self, instance):
        return instance.created_at.strftime("%B %d, %Y")

    def get_answers_count(self, instance):
        return instance.answers.count()

    def get_user_has_answered(self, instance):
        request = self.context.get("request")
        return instance.answers.filter(author=request.user).exists()

class ExamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Exam
        fields = "__all__"


class QuestionLabelSerializer(serializers.ModelSerializer):
    count_votes = serializers.SerializerMethodField()

    def get_count_votes(self, instance):
        label_value = instance.labelValue
        if str(label_value).replace('.','',1).isdigit():
            # In case the label has a numeric value, we calculate the average of the given values, so this return the total number of values.
            return QuestionLabel.objects.filter(labelName=instance.labelName, questionId=instance.questionId).count()
        else:
            # In case the label is not numeric, namely a string, we calculate the max appearances of the given string, so this return the number of appearances of given string.
            return QuestionLabel.objects.filter(labelName=instance.labelName, labelValue=instance.labelValue, questionId=instance.questionId).count()

    class Meta:
        model = QuestionLabel
        fields = "__all__"


class LabelListSerializer(serializers.ModelSerializer):
    possibleValues = serializers.StringRelatedField(many=True)

    class Meta:
        model = Label
        fields = "__all__"
        

class QuestionTopicListSerializer(serializers.ModelSerializer):
    count_votes = serializers.SerializerMethodField()

    class Meta:
        model = QuestionTopic
        fields = "__all__"
    
    def get_count_votes(self, instance):
        return QuestionTopic.objects.filter(topicName=instance.topicName, questionId=instance.questionId).count()

class BreadcrumbsSerializer(serializers.ModelSerializer):
    schoolName = serializers.SerializerMethodField()
    facultyName = serializers.SerializerMethodField()
        

    class Meta:
        model = Exam
        fields = "__all__"

    def get_schoolName(self, instance):
        return instance.courseName.schoolName.__str__()
    
    def get_facultyName(self, instance):
        return instance.courseName.schoolName.facultyName.__str__()


