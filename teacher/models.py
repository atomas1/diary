from django.contrib.auth import get_user_model
from django.db import models
from student.models import *


class Teacher(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    phone = models.CharField(max_length=24)

    class Degree(models.IntegerChoices):
        MASTER = -1
        DOCTOR = 0
        PROFESSOR = 1
        OTHER = 2

    degree = models.IntegerField(choices=Degree.choices, default=-1)
    items = models.ManyToManyField(Item, through='TeacherItemYear', related_name='teacher_items')

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class TeacherItemYear(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)


class Rating(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    date = models.DateField()
    value = models.DecimalField(max_digits=3, decimal_places=1)

    def __str__(self):
        return f"{self.student} {self.date}: {self.value}"


class Lesson(models.Model):
    localization = models.ForeignKey('Localization', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    reunion = models.ForeignKey('Reunion', on_delete=models.CASCADE)
    present_students = models.ManyToManyField(Student, related_name='lesson_present_students')
    topic = models.CharField(max_length=128)
    date_time = models.DateTimeField()
    references = models.FileField(upload_to="student")

    def __str__(self):
        return f"{self.item} - {self.topic}"


class Reunion(models.Model):
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    start_at = models.DateField()
    finish_at = models.DateField()

    def __str__(self):
        return f"{self.academic_year} {self.level}: {self.start_at} - {self.finish_at}"


class Localization(models.Model):
    name = models.CharField(max_length=128)
    address = models.TextField()

    def __str__(self):
        return f"{self.name}"


class Exam(models.Model):
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    localization = models.ForeignKey(Localization, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    students = models.ManyToManyField(Student, through='StudentExam')

    def __str__(self):
        return f"{self.academic_year} - {self.item}"


class StudentExam(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    is_passed = models.BooleanField(default=False)
