from django.contrib.auth.mixins import UserPassesTestMixin

from student.models import Student
from teacher.models import Teacher
from django.conf import settings


class TeacherTestMixin(UserPassesTestMixin):
    login_url = settings.LOGIN_URL

    def test_func(self):
        try:
            teacher = self.request.user.teacher
            return True and self.request.user.is_authenticated
        except AttributeError:
            return False

    def is_teacher(self):
        try:
            teacher = self.request.user.teacher
            return True and self.request.user.is_authenticated
        except AttributeError:
            return False


class StudentTestMixin(UserPassesTestMixin):
    login_url = settings.LOGIN_URL

    def test_func(self):
        try:
            student = self.request.user.student
            return True and self.request.user.is_authenticated
        except AttributeError:
            return False


class SuperUserTestMixin(UserPassesTestMixin):
    login_url = settings.LOGIN_URL

    def test_func(self):
        return self.request.user.is_superuser
