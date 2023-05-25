from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, User
from django.db import models


class Student(models.Model):
    class Confession(models.IntegerChoices):
        NOT_DEFINED = -1
        ROMAN_CATHOLIC = 0
        GREEK_CATHOLIC = 1
        ORTHODOX = 2
        OTHER = 3

    class Education(models.IntegerChoices):
        HIGHER = -1
        SECONDARY = 0
        VOCATIONAL = 1
        PRIMARY = 2
        OTHER = 3

    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    phone = models.CharField(max_length=24)
    birth_date = models.DateField()
    confession = models.IntegerField(choices=Confession.choices, default=-1)
    address = models.TextField(null=True, blank=True)
    workplace = models.TextField(null=True, blank=True)
    comments = models.TextField(null=True, blank=True);
    index = models.CharField(max_length=24, null=True, blank=True)
    diploma = models.CharField(max_length=24, null=True, blank=True)
    level = models.ForeignKey('Level', related_name='current_student_level', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} - level {self.level}"





class AcademicYear(models.Model):
    name = models.CharField(max_length=12)
    started_at = models.DateField()
    finished_at = models.DateField()
    students = models.ManyToManyField(Student, related_name='year_students')
    items = models.ManyToManyField('Item', related_name='year_items', through='StudentItemYear')

    def __str__(self):
        return f'{self.name}'


class Level(models.Model):
    class LevelNumber(models.IntegerChoices):
        FIRST = 1
        SECOND = 2
        LAST = 3

    level_number = models.IntegerField(choices=LevelNumber.choices, default=1)

    def __str__(self):
        return f"{self.level_number}"


class Item(models.Model):
    name = models.CharField(max_length=128)
    students = models.ManyToManyField(Student, through='StudentItemYear')

    def __str__(self):
        return f"{self.name}"




class StudentItemYear(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)



