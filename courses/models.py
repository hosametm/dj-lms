from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return (
            self.user.get_full_name()
            if self.user.get_full_name()
            else self.user.username
        )


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()

    def __str__(self):
        return (
            self.user.get_full_name()
            if self.user.get_full_name()
            else self.user.username
        )


class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    teacher = models.ForeignKey(Teacher, related_name="courses", on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Enrollment(models.Model):
    student = models.ForeignKey(
        Student, related_name="enrollments", on_delete=models.CASCADE
    )
    course = models.ForeignKey(
        Course, related_name="enrollments", on_delete=models.CASCADE
    )
    enrollment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.course}"


class Lesson(models.Model):
    title = models.CharField(max_length=255)
    course = models.ForeignKey(Course, related_name="lessons", on_delete=models.CASCADE)
    media = models.FileField(upload_to="media", blank=True)
    media_type = models.CharField(
        max_length=10,
        blank=True,
        choices=[("video", "video"), ("audio", "audio"), ("pdf", "pdf")],
    )

    def __str__(self):
        return self.title


class StudentProgress(models.Model):
    student = models.ForeignKey(
        Student, related_name="progress", on_delete=models.CASCADE
    )
    lesson = models.ForeignKey(
        Lesson, related_name="progress", on_delete=models.CASCADE
    )
    date_completed = models.DateTimeField(auto_now_add=True)
