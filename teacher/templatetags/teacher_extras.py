from django import template

from student.models import AcademicYear, Item
from teacher.models import Lesson

register = template.Library()


@register.filter
def for_student(ratings, student):
    return ratings.filter(student=student)


@register.filter
def for_academic_year(students, year):
    current_academic_year = AcademicYear.objects.filter(
        name=year).first()
    items = Item.objects.filter(academicyears__in=[current_academic_year]).distinct().order_by(
        'name')
    students = students.filter(academic_years__in=[current_academic_year])
    for student in students:
        student.items_p=[]
        for item in items:
            not_present = Lesson.objects.filter(item=item).filter(
                reunion__academic_year=current_academic_year).distinct().count() - Lesson.objects.filter(
                present_students__in=[student]).filter(item=item).filter(
                reunion__academic_year=current_academic_year).distinct().count()
            student.items_p.append({'ide': item.pk, 'not_present': not_present})
    return students
