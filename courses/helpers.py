from django.db.models import Count, F

def get_course_students_progress(course, student=None):
    students_data = []
    lesson_count = course.lessons.count() if course.lessons else 0
    if not student:
        enrollments = course.enrollments.annotate(
            progress_count=Count(
                "student__progress",
                filter=F("student__progress__lesson__course_id") == course.id,
            )
        )
    else:
        enrollments = course.enrollments.filter(student=student).annotate(
            progress_count=Count(
                "student__progress",
                filter=F("student__progress__lesson__course_id") == course.id,
            )
        )
    students_data = [
        {
            "student": enrollment.student.user.username,
            "progress": (
                f"{(enrollment.progress_count / lesson_count) * 100:.2f}%"
                if lesson_count > 0
                else "0%"
            ),
        }
        for enrollment in enrollments
    ]
    
    return students_data