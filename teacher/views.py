from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import DateInput, ModelMultipleChoiceField, SelectMultiple
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView

from .forms import RatingForm, LessonForm, LessonUpdateForm
from .models import Rating, Teacher, Lesson
from student.models import Item, Student, AcademicYear


# Create your views here.
class Home(LoginRequiredMixin, View):
    def get(self, request):
        is_teacher = self.request.session.get('is_teacher')
        current_academic_year = AcademicYear.objects.filter(
            name=self.request.session.get('current_academic_year')).first()
        items = Item.objects.filter(
            teachers__in=[self.request.user.teacher]).filter(academicyears__in=[current_academic_year]).order_by(
            'name')
        students = []
        for item in items:
            for student in item.students.filter(academic_years__in=[current_academic_year]).order_by('user__last_name'):
                student.item = item
                student.item.not_present = item.lessons.filter(
                    reunion__academic_year=current_academic_year).count() - Lesson.objects.filter(item=item).filter(
                    reunion__academic_year=current_academic_year).filter(present_students__in=[student]).count()
                students.append(student)
        ratings = Rating.objects.filter(item__in=items).filter(teacher=request.user.teacher)
        return render(request, 'teacher/home.html',
                      context={'items': items, 'students': students, 'is_teacher': is_teacher, 'ratings': ratings})


class RatingCreateView(LoginRequiredMixin, CreateView):
    model = Rating
    form_class = RatingForm
    template_name = 'teacher/rating_create.html'
    success_url = reverse_lazy('teacher:home')

    def get_form(self, *args, **kwargs):
        current_academic_year = AcademicYear.objects.filter(
            name=self.request.session.get('current_academic_year')).first()
        form = super(RatingCreateView, self).get_form(*args, **kwargs)
        items = Item.objects.filter(
            teachers__in=[self.request.user.teacher]).filter(academicyears__in=[current_academic_year]).order_by(
            'name')
        form.fields['item'].queryset = items
        form.fields['teacher'].queryset = Teacher.objects.filter(pk=self.request.user.teacher.pk)
        students = Student.objects.filter(items__in=items)
        form.fields['student'].queryset = students
        return form

    def get_context_data(self, *args, **kwargs):
        context = super(RatingCreateView, self).get_context_data(*args, **kwargs)
        context['is_teacher'] = self.request.session.get('is_teacher')
        return context
    # login_url = reverse_lazy('users:login')


class LessonCreateView(LoginRequiredMixin, CreateView):
    model = Lesson
    form_class = LessonForm
    template_name = 'teacher/lesson_create.html'
    success_url = reverse_lazy('teacher:lessons')

    def get_form(self, *args, **kwargs):
        current_academic_year = AcademicYear.objects.filter(
            name=self.request.session.get('current_academic_year')).first()
        form = super(LessonCreateView, self).get_form(*args, **kwargs)
        items = Item.objects.filter(
            teachers__in=[self.request.user.teacher]).filter(academicyears__in=[current_academic_year]).order_by(
            'name')
        form.fields['item'].queryset = items
        form.fields['teacher'].queryset = Teacher.objects.filter(pk=self.request.user.teacher.pk)
        return form

    def get_context_data(self, *args, **kwargs):
        context = super(LessonCreateView, self).get_context_data(*args, **kwargs)
        context['is_teacher'] = self.request.session.get('is_teacher')
        return context


class RatingUpdateView(LoginRequiredMixin, UpdateView):
    model = Rating
    form_class = RatingForm
    template_name = 'teacher/rating_create.html'
    success_url = reverse_lazy('teacher:home')

    def get_form(self, *args, **kwargs):
        current_academic_year = AcademicYear.objects.filter(
            name=self.request.session.get('current_academic_year')).first()
        form = super(RatingUpdateView, self).get_form(*args, **kwargs)
        items = Item.objects.filter(
            teachers__in=[self.request.user.teacher]).filter(academicyears__in=[current_academic_year]).order_by(
            'name')
        form.fields['item'].queryset = items
        form.fields['teacher'].queryset = Teacher.objects.filter(pk=self.request.user.teacher.pk)
        students = Student.objects.filter(items__in=items)
        form.fields['student'].queryset = students
        return form

    def get_context_data(self, *args, **kwargs):
        context = super(RatingUpdateView, self).get_context_data(*args, **kwargs)
        context['is_teacher'] = self.request.session.get('is_teacher')
        return context


class TeacherLessonsView(LoginRequiredMixin, View):
    def get(self, request):
        current_academic_year = AcademicYear.objects.filter(
            name=self.request.session.get('current_academic_year')).first()
        lessons = Lesson.objects.filter(reunion__academic_year=current_academic_year).filter(
            teacher=self.request.user.teacher).order_by('-date_time')
        is_teacher = self.request.session.get('is_teacher')
        return render(request, 'teacher/lessons.html', context={'lessons': lessons, 'is_teacher': is_teacher})


class LessonUpdateView(LoginRequiredMixin, UpdateView):
    model = Lesson
    form_class = LessonForm
    template_name = 'teacher/lesson_create.html'
    success_url = reverse_lazy('teacher:lessons')

    def get_form(self, *args, **kwargs):
        current_academic_year = AcademicYear.objects.filter(
            name=self.request.session.get('current_academic_year')).first()
        form = super(LessonUpdateView, self).get_form(*args, **kwargs)
        items = Item.objects.filter(
            teachers__in=[self.request.user.teacher]).filter(academicyears__in=[current_academic_year]).order_by(
            'name')
        form.fields['item'].queryset = items
        form.fields['teacher'].queryset = Teacher.objects.filter(pk=self.request.user.teacher.pk)
        form.fields['present_students'] = ModelMultipleChoiceField(label="Present students", widget=SelectMultiple,
                                                                   queryset=Student.objects.filter(items__in=items))

        return form

    def get_context_data(self, *args, **kwargs):
        context = super(LessonUpdateView, self).get_context_data(*args, **kwargs)
        context['is_teacher'] = self.request.session.get('is_teacher')
        return context
