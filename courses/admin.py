from django.contrib import admin
from .models import Course, Lesson, Student, Teacher, StudentProgress, Enrollment

admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(StudentProgress)
admin.site.register(Enrollment)
