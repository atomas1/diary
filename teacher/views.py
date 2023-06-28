from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.forms import ModelMultipleChoiceField, SelectMultiple
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView

from .forms import RatingForm, LessonForm, LessonUpdateForm, ExamForm, EmptyForm
from .models import Rating, Teacher, Lesson, Exam, StudentExam
from student.models import Item, Student, AcademicYear


# Create your views here.
class Home(LoginRequiredMixin, View):
    """Default view for teacher app. List of teachers's students with their ratings"""

    def get(self, request):
        is_teacher = self.request.session.get('is_teacher')
        current_academic_year = AcademicYear.objects.filter(
            name=self.request.session.get('current_academic_year')).first()
        if is_teacher:
            items = Item.objects.filter(
                Q(teachers__in=[self.request.user.teacher]) & Q(
                    academicyears__in=[current_academic_year])).distinct().order_by('name')
            ratings = Rating.objects.filter(item__in=items).filter(teacher=request.user.teacher)

        else:
            items = []
            ratings = []

        return render(request, 'teacher/home.html',
                      context={'items': items, 'is_teacher': is_teacher, 'ratings': ratings})


class RatingCreateView(LoginRequiredMixin, CreateView):
    """generic view based rating create view"""
    model = Rating
    form_class = RatingForm
    template_name = 'teacher/rating_create.html'
    success_url = reverse_lazy('teacher:home')

    def get_form(self, *args, **kwargs):
        try:
            is_teacher = self.request.user.teacher.degree
        except AttributeError:
            return EmptyForm()
        current_academic_year = AcademicYear.objects.filter(
            name=self.request.session.get('current_academic_year')).first()
        form = super(RatingCreateView, self).get_form(*args, **kwargs)
        items = Item.objects.filter(
            teachers__in=[self.request.user.teacher]).filter(
            academicyears__in=[current_academic_year]).distinct().order_by(
            'name')
        form.fields['item'].queryset = items

        form.fields['teacher'].queryset = Teacher.objects.filter(pk=self.request.user.teacher.pk)
        students = Student.objects.filter(items__in=items).distinct().order_by('user__last_name')
        form.fields['student'].queryset = students
        return form

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['is_teacher'] = self.request.session.get('is_teacher')
        context['is_student'] = self.request.session.get('is_student')
        return context


class LessonCreateView(LoginRequiredMixin, CreateView):
    """View for creating lesson"""
    model = Lesson
    form_class = LessonForm
    template_name = 'teacher/lesson_create.html'
    success_url = reverse_lazy('teacher:lessons')

    def get_form(self, *args, **kwargs):
        try:
            is_teacher = self.request.user.teacher.degree
        except AttributeError:
            return EmptyForm()
        current_academic_year = AcademicYear.objects.filter(
            name=self.request.session.get('current_academic_year')).first()
        form = super().get_form(*args, **kwargs)
        items = Item.objects.filter(
            teachers__in=[self.request.user.teacher]).filter(
            academicyears__in=[current_academic_year]).distinct().order_by(
            'name')
        form.fields['item'].queryset = items
        form.fields['teacher'].queryset = Teacher.objects.filter(pk=self.request.user.teacher.pk)
        return form

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['is_teacher'] = self.request.session.get('is_teacher')
        return context


class RatingUpdateView(LoginRequiredMixin, UpdateView):
    """view for updating student's ratings"""
    model = Rating
    form_class = RatingForm
    template_name = 'teacher/rating_create.html'
    success_url = reverse_lazy('teacher:home')

    def get_form(self, *args, **kwargs):
        try:
            is_teacher = self.request.user.teacher.degree
        except AttributeError:
            return EmptyForm()
        current_academic_year = AcademicYear.objects.filter(
            name=self.request.session.get('current_academic_year')).first()
        form = super().get_form(*args, **kwargs)
        items = Item.objects.filter(
            teachers__in=[self.request.user.teacher]).filter(
            academicyears__in=[current_academic_year]).distinct().order_by(
            'name')
        form.fields['item'].queryset = items
        form.fields['teacher'].queryset = Teacher.objects.filter(pk=self.request.user.teacher.pk)
        students = Student.objects.filter(items__in=items).distinct().order_by('user__last_name')
        form.fields['student'].queryset = students
        return form

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['is_teacher'] = self.request.session.get('is_teacher')
        return context


class TeacherLessonsView(LoginRequiredMixin, View):
    """Lessons of logged teacher"""

    def get(self, request):
        current_academic_year = AcademicYear.objects.filter(
            name=self.request.session.get('current_academic_year')).first()
        lessons = Lesson.objects.filter(reunion__academic_year=current_academic_year).filter(
            teacher=self.request.user.teacher).order_by('-date_time')
        is_teacher = self.request.session.get('is_teacher')
        return render(request, 'teacher/lessons.html', context={'lessons': lessons, 'is_teacher': is_teacher})


class LessonUpdateView(LoginRequiredMixin, UpdateView):
    """View for updating lesson data based on specific form"""
    model = Lesson
    form_class = LessonUpdateForm
    template_name = 'teacher/lesson_create.html'
    success_url = reverse_lazy('teacher:lessons')

    def get_form(self, *args, **kwargs):
        try:
            is_teacher = self.request.user.teacher.degree
        except AttributeError:
            return EmptyForm()
        current_academic_year = AcademicYear.objects.filter(
            name=self.request.session.get('current_academic_year')).first()
        form = super().get_form(*args, **kwargs)
        items = Item.objects.filter(
            teachers__in=[self.request.user.teacher]).filter(
            academicyears__in=[current_academic_year]).distinct().order_by(
            'name')
        form.fields['item'].queryset = items
        form.fields['teacher'].queryset = Teacher.objects.filter(pk=self.request.user.teacher.pk)
        form.fields['present_students'] = ModelMultipleChoiceField(label="Present students", widget=SelectMultiple,
                                                                   queryset=Student.objects.filter(
                                                                       items__in=items).distinct().order_by(
                                                                       'user__last_name'))

        return form

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['is_teacher'] = self.request.session.get('is_teacher')
        return context


class ExamCreateView(LoginRequiredMixin, CreateView):
    """Logged techer can create exams for his items"""
    model = Exam
    form_class = ExamForm
    template_name = 'teacher/exam_create.html'
    success_url = reverse_lazy('teacher:lessons')

    def get_form(self, *args, **kwargs):
        try:
            is_teacher = self.request.user.teacher.degree
        except AttributeError:
            return EmptyForm()
        current_academic_year = AcademicYear.objects.filter(
            name=self.request.session.get('current_academic_year')).first()
        form = super().get_form(*args, **kwargs)
        items = Item.objects.filter(
            teachers__in=[self.request.user.teacher]).filter(
            academicyears__in=[current_academic_year]).distinct().order_by(
            'name')
        students = Student.objects.filter(items__in=items).filter(
            academic_years__in=[current_academic_year]).distinct().order_by(
            'user__last_name')
        form.fields['academic_year'].queryset = AcademicYear.objects.filter(pk=current_academic_year.pk)
        form.fields['item'].queryset = items
        form.fields['students'].queryset = students
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_teacher'] = self.request.session.get('is_teacher')
        return context


class ExamUpdateView(LoginRequiredMixin, UpdateView):
    """Logged teacher can update exams for his items"""
    model = Exam
    form_class = ExamForm
    template_name = 'teacher/exam_create.html'
    success_url = reverse_lazy('teacher:lessons')

    def get_form(self, *args, **kwargs):
        try:
            is_teacher = self.request.user.teacher.degree
        except AttributeError:
            return EmptyForm()
        current_academic_year = AcademicYear.objects.filter(
            name=self.request.session.get('current_academic_year')).first()
        form = super().get_form(*args, **kwargs)
        items = Item.objects.filter(
            teachers__in=[self.request.user.teacher]).filter(
            academicyears__in=[current_academic_year]).distinct().order_by(
            'name')
        students = Student.objects.filter(items__in=items).filter(
            academic_years__in=[current_academic_year]).distinct().order_by(
            'user__last_name')
        form.fields['academic_year'].queryset = AcademicYear.objects.filter(pk=current_academic_year.pk)
        form.fields['item'].queryset = items
        form.fields['students'].queryset = students
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_teacher'] = self.request.session.get('is_teacher')
        return context


class TeacherExamsView(LoginRequiredMixin, View):
    """List of exams for logged teacher lessons"""

    def get(self, request):
        current_academic_year = AcademicYear.objects.filter(
            name=self.request.session.get('current_academic_year')).first()
        items = Item.objects.filter(
            teachers__in=[self.request.user.teacher]).filter(academicyears__in=[current_academic_year]).order_by(
            'name')
        exams = Exam.objects.filter(academic_year=current_academic_year).filter(item__in=items).order_by('-date_time')
        is_teacher = self.request.session.get('is_teacher')
        return render(request, 'teacher/exams.html', context={'exams': exams, 'is_teacher': is_teacher})


class ExamRatingUpdate(LoginRequiredMixin, UpdateView):
    """Logged teacher can update exam's ratings"""
    model = StudentExam
    fields = ['student', 'exam', 'rating', 'is_passed']
    template_name = 'teacher/exam_create.html'
    success_url = reverse_lazy('teacher:exams')

    def get_form(self, *args, **kwargs):
        try:
            is_teacher = self.request.user.teacher.degree
        except AttributeError:
            return EmptyForm()
        current_academic_year = AcademicYear.objects.filter(
            name=self.request.session.get('current_academic_year')).first()
        form = super().get_form(*args, **kwargs)
        items = Item.objects.filter(
            teachers__in=[self.request.user.teacher]).filter(
            academicyears__in=[current_academic_year]).distinct().order_by(
            'name')
        students = Student.objects.filter(items__in=items).filter(
            academic_years__in=[current_academic_year]).distinct().order_by(
            'user__last_name')
        form.fields['student'].queryset = students
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_teacher'] = self.request.session.get('is_teacher')
        return context
