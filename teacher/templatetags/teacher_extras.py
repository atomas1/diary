from django import template

register = template.Library()


@register.filter
def for_student(ratings, student):
    return ratings.filter(student=student)
