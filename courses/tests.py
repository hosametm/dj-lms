from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from courses.models import Course, Teacher


class CourseTests(APITestCase):

    def setUp(self):
        self.teacher_user = User.objects.create_user(
            username="teacher", password="password"
        )
        self.teacher = Teacher.objects.create(user=self.teacher_user, bio="Teacher bio")

    def test_create_course(self):
        data = {
            "title": "New Course",
            "description": "A new course description",
            "teacher": self.teacher.id,
        }
        response = self.client.post("/api/courses/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "New Course")
        self.assertEqual(response.data["teacher"], self.teacher.id)


from courses.models import Student


class EnrollmentTests(APITestCase):

    def setUp(self):
        self.student_user = User.objects.create_user(
            username="student", password="password"
        )
        self.student = Student.objects.create(user=self.student_user)
        self.teacher_user = User.objects.create_user(
            username="teacher", password="password"
        )
        self.teacher = Teacher.objects.create(user=self.teacher_user, bio="Teacher bio")
        self.course = Course.objects.create(
            title="Test Course", description="Course description", teacher=self.teacher
        )

    def test_enroll_student(self):
        data = {"student": self.student.id}
        url = f"/api/courses/{self.course.id}/enroll/"
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Enrolled successfully.")

    def test_enroll_student_already_enrolled(self):
        self.course.enrollments.create(student=self.student)
        data = {"student": self.student.id}
        url = f"/api/courses/{self.course.id}/enroll/"
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Already enrolled.")


class EnrolledStudentsTests(APITestCase):

    def setUp(self):
        self.student_user = User.objects.create_user(
            username="student", password="password"
        )
        self.student = Student.objects.create(user=self.student_user)
        self.teacher_user = User.objects.create_user(
            username="teacher", password="password"
        )
        self.teacher = Teacher.objects.create(user=self.teacher_user, bio="Teacher bio")
        self.course = Course.objects.create(
            title="Test Course", description="Course description", teacher=self.teacher
        )
        self.course.enrollments.create(student=self.student)

    def test_enrolled_students(self):
        url = f"/api/courses/{self.course.id}/enrolled-students/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["enrolled_students"]), 1)
        self.assertEqual(response.data["enrolled_students"][0]["id"], self.student.id)


from django.core.files.uploadedfile import SimpleUploadedFile
from courses.models import Lesson


class LessonTests(APITestCase):

    def setUp(self):
        self.student_user = User.objects.create_user(
            username="student", password="password"
        )
        self.student = Student.objects.create(user=self.student_user)
        self.teacher_user = User.objects.create_user(
            username="teacher", password="password"
        )
        self.teacher = Teacher.objects.create(user=self.teacher_user, bio="Teacher bio")
        self.course = Course.objects.create(
            title="Test Course", description="Course description", teacher=self.teacher
        )

    def test_create_lesson(self):
        file = SimpleUploadedFile(
            "test_video.mp4", b"file_content", content_type="video/mp4"
        )
        data = {
            "title": "New Lesson",
            "media": file,
            "media_type": "video",
        }
        url = f"/api/courses/{self.course.id}/lessons/"
        response = self.client.post(url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "New Lesson")
        self.assertEqual(response.data["media_type"], "video")


class ListLessonsTests(APITestCase):

    def setUp(self):
        self.student_user = User.objects.create_user(
            username="student", password="password"
        )
        self.student = Student.objects.create(user=self.student_user)
        self.teacher_user = User.objects.create_user(
            username="teacher", password="password"
        )
        self.teacher = Teacher.objects.create(user=self.teacher_user, bio="Teacher bio")
        self.course = Course.objects.create(
            title="Test Course", description="Course description", teacher=self.teacher
        )
        self.lesson = Lesson.objects.create(
            title="Test Lesson",
            course=self.course,
            media_type="video",
            media="test_video.mp4",
        )

    def test_list_lessons(self):
        url = f"/api/courses/{self.course.id}/lessons/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("response.data")
        print(response.data)
        self.assertEqual(response.data['results'][0]["title"], "Test Lesson")


class SaveProgressTests(APITestCase):

    def setUp(self):
        self.student_user = User.objects.create_user(
            username="student", password="password"
        )
        self.student = Student.objects.create(user=self.student_user)
        self.teacher_user = User.objects.create_user(
            username="teacher", password="password"
        )
        self.teacher = Teacher.objects.create(user=self.teacher_user, bio="Teacher bio")
        self.course = Course.objects.create(
            title="Test Course", description="Course description", teacher=self.teacher
        )
        self.lesson = Lesson.objects.create(
            title="Test Lesson",
            course=self.course,
            media_type="video",
            media="test_video.mp4",
        )
        self.course.enrollments.create(student=self.student)

    def test_save_progress(self):
        data = {"student": self.student.id}
        url = f"/api/courses/{self.course.id}/lessons/{self.lesson.id}/save-progress/"
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Progress saved successfully.")


class SaveProgressNotEnrolledTests(APITestCase):

    def setUp(self):
        self.student_user = User.objects.create_user(
            username="student", password="password"
        )
        self.student = Student.objects.create(user=self.student_user)
        self.teacher_user = User.objects.create_user(
            username="teacher", password="password"
        )
        self.teacher = Teacher.objects.create(user=self.teacher_user, bio="Teacher bio")
        self.course = Course.objects.create(
            title="Test Course", description="Course description", teacher=self.teacher
        )
        self.lesson = Lesson.objects.create(
            title="Test Lesson",
            course=self.course,
            media_type="video",
            media="test_video.mp4",
        )

    def test_save_progress_not_enrolled(self):
        data = {"student": self.student.id}
        url = f"/api/courses/{self.course.id}/lessons/{self.lesson.id}/save-progress/"
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class EnrollInNonExistentCourseTests(APITestCase):

    def setUp(self):
        self.student_user = User.objects.create_user(
            username="student", password="password"
        )
        self.student = Student.objects.create(user=self.student_user)

    def test_enroll_in_non_existent_course(self):
        data = {"student": self.student.id}
        url = "/api/courses/999/enroll/"  # Non-existing course ID
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["detail"], "Course not found.")
