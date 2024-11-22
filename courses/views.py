from rest_framework import viewsets
from .models import Course, Lesson, Student
from .serializers import (
    CourseSerializer,
    LessonSerializer,
    StudentSerializer,
)
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.decorators import action
from rest_framework.response import Response
from .helpers import get_course_students_progress


class CoursesViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all().prefetch_related("lessons")
    serializer_class = CourseSerializer

    # enroll action
    @action(detail=True, methods=["POST"], url_path="enroll")
    def enroll(self, request, pk=None):
        try:
            course = Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            raise NotFound("Course not found.")
        student = request.data.get("student")
        if not student:
            raise ValidationError("student is required.")
        if course.enrollments.filter(student_id=student).exists():
            return Response({"message": "Already enrolled."})
        course.enrollments.create(student_id=student)
        return Response({"message": "Enrolled successfully."})

    @action(detail=True, methods=["GET"], url_path="enrolled-students")
    def enrolled_students(self, request, pk=None):
        try:
            course = Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            raise NotFound("Course not found.")
        enrolled_students = course.enrollments.values_list("student_id", flat=True)
        student_ids = list(enrolled_students)
        students = Student.objects.filter(id__in=student_ids)
        students_data = StudentSerializer(students, many=True).data
        return Response({"enrolled_students": students_data})

    # get students progress
    @action(detail=True, methods=["GET"], url_path="students-progress")
    def students_progress(self, request, pk=None):
        student = request.query_params.get("student")
        try:
            course = Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            raise NotFound("Course not found.")
        if student:
            student = Student.objects.filter(pk=student).first()
            if not student:
                raise NotFound("Student not found.")

        students_data = get_course_students_progress(course, student)
        return Response({"students_progress": students_data})


class LessonsViewSet(viewsets.ModelViewSet):
    serializer_class = LessonSerializer

    def get_queryset(self):
        course_id = self.kwargs.get("course_pk")
        if not Course.objects.filter(pk=course_id).exists():
            raise ValidationError("Course not found.")
        return Lesson.objects.filter(course_id=course_id)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["course_pk"] = self.kwargs.get("course_pk")
        return context

    def perform_create(self, serializer):
        course_id = self.kwargs.get("course_pk")
        try:
            course = Course.objects.get(pk=course_id)
        except Course.DoesNotExist:
            raise NotFound("Course not found.")
        serializer.save(course=course)

    @action(detail=True, methods=["POST"], url_path="save-progress")
    def save_progress(self, request, course_pk=None, lesson_pk=None):
        """this could be run manually by students or automatically by FE when they complete a lesson to save their progress"""
        try:
            lesson = Lesson.objects.get(pk=lesson_pk)
        except Lesson.DoesNotExist:
            raise NotFound("Lesson not found.")
        student = request.data.get("student")
        if not student:
            raise ValidationError("student is required.")
        if not lesson.course.enrollments.filter(student_id=student).exists():
            raise ValidationError("Student is not enrolled in the course.")
        if lesson.progress.filter(student_id=student).exists():
            return Response({"message": "Progress already saved."})
        lesson.progress.create(student_id=student)
        return Response({"message": "Progress saved successfully."})
