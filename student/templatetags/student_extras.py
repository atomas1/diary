from django import template

register = template.Library()


@register.filter
def in_item(ratings, item):
    return ratings.filter(item=item)


@register.filter
def in_exam(ratings, exam):
    return ratings.filter(exam=exam)
