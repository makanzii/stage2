from datetime import datetime

from rest_framework import serializers
from .models import User, Course, Post, Reply, Quiz


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['avatar', 'email', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value


class CourseSerializer(serializers.ModelSerializer):
    enrolled = serializers.SerializerMethodField()
    quizzes = serializers.SerializerMethodField()

    def get_quizzes(self, obj):
        return QuizSerializer(Quiz.objects.filter(course_id=obj.id), many=True).data

    def get_enrolled(self, obj):
        if self.context['request'].user:
            user = self.context['request'].user
            return user.courses.filter(id=obj.id).exists()
        return False

    class Meta:
        model = Course
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Post
        fields = '__all__'


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class ReplySerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Reply
        fields = '__all__'


class ReplyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = '__all__'


class QuizSerializer(serializers.ModelSerializer):
    available = serializers.SerializerMethodField()

    def get_available(self, obj):
        # check date
        curr_date = datetime.now().date()
        return obj.date > curr_date

    class Meta:
        model = Quiz
        fields = '__all__'
