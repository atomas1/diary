from django.db import models
from django.conf import settings


class Student(models.Model):
    """school student model inherited from the user model"""
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

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    academic_years = models.ManyToManyField('AcademicYear', related_name='students')
    phone = models.CharField(max_length=24)
    birth_date = models.DateField()
    confession = models.IntegerField(choices=Confession.choices, default=-1)
    education = models.IntegerField(choices=Education.choices, default=-1)
    address = models.TextField(blank=True)
    workplace = models.TextField(blank=True)
    comments = models.TextField(blank=True);
    index = models.CharField(max_length=24, blank=True, unique=True)
    diploma = models.CharField(max_length=24, blank=True, unique=False)
    level = models.ForeignKey('Level', related_name='students', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} - level {self.level}"


class AcademicYear(models.Model):
    """We can manage academic years"""
    name = models.CharField(max_length=12)
    started_at = models.DateField()
    finished_at = models.DateField()
    items = models.ManyToManyField('Item', related_name='academicyears', through='StudentItemYear')

    def __str__(self):
        return f'{self.name}'


class Level(models.Model):
    """The school has three levels"""
    class LevelNumber(models.IntegerChoices):
        FIRST = 1
        SECOND = 2
        LAST = 3

    level_number = models.IntegerField(choices=LevelNumber.choices, default=1)

    def __str__(self):
        return f"{self.level_number}"


class Item(models.Model):
    """Model to manage school items"""
    name = models.CharField(max_length=128)
    students = models.ManyToManyField(Student, through='StudentItemYear', related_name='items')

    def __str__(self):
        return f"{self.name}"


class StudentItemYear(models.Model):
    """model describing M2M relationship between student, academic years and items """
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)

    class Meta:
        """only one item student pair is possible in given academic year"""
        unique_together = ('student', 'item', 'academic_year',)

    def __str__(self):
        return self.student.user.first_name + " " + self.student.user.last_name + " " + " " + self.item.name + " " + self.academic_year.name
