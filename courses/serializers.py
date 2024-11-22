from rest_framework import serializers
from .models import Course, Lesson, StudentProgress, Student, Teacher
from django.contrib.auth.models import User


class LessonSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=255, required=True)
    media = serializers.FileField(required=True)

    class Meta:
        model = Lesson
        fields = ["id", "title", "media", "media_type"]

    def validate_media(self, value):
        if value.content_type.split("/")[0] not in ["video", "audio", "pdf"]:
            raise serializers.ValidationError("Invalid media type.")
        return value

    def create(self, validated_data):
        media = validated_data.pop("media")
        validated_data["media_type"] = media.content_type.split("/")[0]
        lesson = Lesson.objects.create(**validated_data, media=media)
        return lesson


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class StudentProgressSerializer(serializers.ModelSerializer):

    class Meta:
        model = StudentProgress
        fields = "__all__"


class StudentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")
    email = serializers.CharField(source="user.email")
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")

    class Meta:
        model = Student
        fields = ["id", "username", "email", "first_name", "last_name"]


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = "__all__"
