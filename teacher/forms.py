from django.forms import DateInput, DateTimeInput
from django.forms import ModelForm, Form

from .models import Rating, Lesson, Exam


class DateInput(DateInput):
    input_type = 'date'


class DateTimeInput(DateTimeInput):
    input_type = 'datetime-local'


class RatingForm(ModelForm):
    class Meta:
        model = Rating
        fields = ('student', 'teacher', 'item', 'date', 'value', 'notice')
        widgets = {
            'date': DateInput(),
        }


class LessonForm(ModelForm):
    class Meta:
        model = Lesson
        fields = (
            'localization', 'reunion', 'level', 'date_time', 'teacher', 'item', 'topic', 'references')
        widgets = {
            'date_time': DateTimeInput(),
        }


class LessonUpdateForm(ModelForm):
    class Meta:
        model = Lesson
        fields = (
            'localization', 'reunion', 'level', 'date_time', 'teacher', 'item', 'topic', 'present_students',
            'references')
        widgets = {
            'date_time': DateTimeInput(),
        }


class ExamForm(ModelForm):
    class Meta:
        model = Exam
        fields = (
            'academic_year', 'localization', 'date_time', 'item', 'students')
        widgets = {
            'date_time': DateTimeInput(),
        }


class EmptyForm(Form):
    pass
