from django.contrib import admin
from .models import Teacher, TeacherItemYear, Localization, Reunion, Exam, StudentExam, Lesson, Rating

admin.site.register(Teacher)
admin.site.register(TeacherItemYear)
admin.site.register(Localization)
admin.site.register(Reunion)
admin.site.register(Exam)
admin.site.register(StudentExam)
admin.site.register(Lesson)
admin.site.register(Rating)


