from django.db import models
from django.conf import settings
from student.models import Item, AcademicYear, Level, Student


class Teacher(models.Model):
    """teachers in shool inherited forom the user model. It is possible the former student to become a teacher"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(max_length=24)

    class Degree(models.IntegerChoices):
        MASTER = -1
        DOCTOR = 0
        PROFESSOR = 1
        OTHER = 2

    degree = models.IntegerField(choices=Degree.choices, default=-1)
    items = models.ManyToManyField(Item, through='TeacherItemYear', related_name='teachers')

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class TeacherItemYear(models.Model):
    """Model describing M2M relationship between Teacher and items in given academic year """
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)

    class Meta:
        """only one entry for item to specific teacher in given academic year is possible"""
        unique_together = ('teacher', 'item', 'academic_year')

    def __str__(self):
        return f"{self.academic_year} - {self.teacher} - {self.item}"


class Rating(models.Model):
    """ratings for students"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='ratings')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='ratings')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='ratings')
    date = models.DateField()
    value = models.DecimalField(max_digits=3, decimal_places=2)
    notice = models.TextField()

    def __str__(self):
        return f"{self.student} - {self.item} - {self.date}: {self.value}"


class Lesson(models.Model):
    """lessons for item in specific reunion"""
    localization = models.ForeignKey('Localization', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='lessons')
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name='lessons')
    reunion = models.ForeignKey('Reunion', on_delete=models.CASCADE, related_name='lessons')
    present_students = models.ManyToManyField(Student, related_name='lessons')
    topic = models.CharField(max_length=128)
    date_time = models.DateTimeField()
    references = models.FileField(upload_to="student", blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='lessons')

    def __str__(self):
        return f"{self.item} - {self.topic}"


class Reunion(models.Model):
    """weekend's reunions"""
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name="reunions")
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name='reunions')
    start_at = models.DateField()
    finish_at = models.DateField()

    def __str__(self):
        return f"{self.academic_year} {self.level}: {self.start_at} - {self.finish_at}"


class Localization(models.Model):
    """Localizations for lessons and exams"""
    name = models.CharField(max_length=128)
    address = models.TextField()

    def __str__(self):
        return f"{self.name}"


class Exam(models.Model):
    """Exams"""
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    localization = models.ForeignKey(Localization, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='exams')
    date_time = models.DateTimeField()
    students = models.ManyToManyField(Student, through='StudentExam', related_name='exams')

    def __str__(self):
        return f"{self.academic_year} - {self.item}"


class StudentExam(models.Model):
    """model describing the M2M relationship beetween student and exam. The rating may be corrected until the exam is marked as passed"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True)
    is_passed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('student', 'exam',)

    def __str__(self):
        return f"{self.student} - {self.exam}: {self.rating}"
