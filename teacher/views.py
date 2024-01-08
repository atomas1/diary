from django.db.models import Q
from django.forms import ModelMultipleChoiceField, SelectMultiple
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, UpdateView, DetailView

from utlis import TeacherTestMixin, SuperUserTestMixin
from .forms import RatingForm, LessonForm, LessonUpdateForm, ExamForm, EmptyForm
from .models import Rating, Teacher, Lesson, Exam, StudentExam
from student.models import Item, Student, AcademicYear


# Create your views here.
class Home(TeacherTestMixin, View):
    """Default view for teacher app. List of teachers's students with their ratings"""

    def get(self, request):
        current_academic_year = AcademicYear.objects.filter(
            name=self.request.session.get('current_academic_year')).first()
        items = Item.objects.filter(
            Q(teachers__in=[self.request.user.teacher]) & Q(
                academicyears__in=[current_academic_year])).distinct().order_by('name')
        ratings = Rating.objects.filter(item__in=items).filter(teacher=request.user.teacher)

        return render(request, 'teacher/home.html',
                      context={'items': items, 'is_teacher': True, 'ratings': ratings})

    def handle_no_permission(self):
        if TeacherTestMixin.is_teacher(self):
            items = []
            ratings = []

            return render(self.request, 'teacher/home.html',
                          context={'items': items, 'is_teacher': True, 'ratings': ratings})
        else:
            return redirect(reverse('users:login'))


class RatingCreateView(TeacherTestMixin, CreateView):
    """generic view based rating create view"""
    model = Rating
    form_class = RatingForm
    template_name = 'teacher/rating_create.html'
    success_url = reverse_lazy('teacher:home')

    def get_form(self, *args, **kwargs):
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

    def handle_no_permission(self):
        if TeacherTestMixin.is_teacher(self):
            return EmptyForm();
        else:
            return redirect(reverse('users:login'))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['is_teacher'] = True
        context['is_student'] = False
        return context


class LessonCreateView(TeacherTestMixin, CreateView):
    """View for creating lesson"""
    model = Lesson
    form_class = LessonForm
    template_name = 'teacher/lesson_create.html'
    success_url = reverse_lazy('teacher:lessons')

    def get_form(self, *args, **kwargs):
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

    def handle_no_permission(self):
        if TeacherTestMixin.is_teacher(self):
            return EmptyForm();
        else:
            return redirect(reverse('users:login'))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['is_teacher'] = True
        return context


class RatingUpdateView(TeacherTestMixin, UpdateView):
    """view for updating student's ratings"""
    model = Rating
    form_class = RatingForm
    template_name = 'teacher/rating_create.html'
    success_url = reverse_lazy('teacher:home')

    def get_form(self, *args, **kwargs):
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

    def handle_no_permission(self):
        if TeacherTestMixin.is_teacher(self):
            return EmptyForm();
        else:
            return redirect(reverse('users:login'))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['is_teacher'] = True
        return context


class TeacherLessonsView(TeacherTestMixin, View):
    """Lessons of logged teacher"""

    def get(self, request):
        current_academic_year = AcademicYear.objects.filter(
            name=self.request.session.get('current_academic_year')).first()
        lessons = Lesson.objects.filter(reunion__academic_year=current_academic_year).filter(
            teacher=self.request.user.teacher).order_by('-date_time')
        is_teacher = True
        return render(request, 'teacher/lessons.html', context={'lessons': lessons, 'is_teacher': is_teacher})


class LessonUpdateView(TeacherTestMixin, UpdateView):
    """View for updating lesson data based on specific form"""
    model = Lesson
    form_class = LessonUpdateForm
    template_name = 'teacher/lesson_create.html'
    success_url = reverse_lazy('teacher:lessons')

    def get_form(self, *args, **kwargs):
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

    def handle_no_permission(self):
        if TeacherTestMixin.is_teacher(self):
            return EmptyForm();
        else:
            return redirect(reverse('users:login'))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['is_teacher'] = True
        return context


class ExamCreateView(TeacherTestMixin, CreateView):
    """Logged techer can create exams for his items"""
    model = Exam
    form_class = ExamForm
    template_name = 'teacher/exam_create.html'
    success_url = reverse_lazy('teacher:lessons')

    def get_form(self, *args, **kwargs):
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

    def handle_no_permission(self):
        if TeacherTestMixin.is_teacher(self):
            return EmptyForm();
        else:
            return redirect(reverse('users:login'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_teacher'] = True
        return context


class ExamUpdateView(TeacherTestMixin, UpdateView):
    """Logged teacher can update exams for his items"""
    model = Exam
    form_class = ExamForm
    template_name = 'teacher/exam_create.html'
    success_url = reverse_lazy('teacher:lessons')

    def get_form(self, *args, **kwargs):
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

    def handle_no_permission(self):
        if TeacherTestMixin.is_teacher(self):
            return EmptyForm();
        else:
            return redirect(reverse('users:login'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_teacher'] = True
        return context


class TeacherExamsView(TeacherTestMixin, View):
    """List of exams for logged teacher lessons"""

    def get(self, request):
        current_academic_year = AcademicYear.objects.filter(
            name=self.request.session.get('current_academic_year')).first()
        items = Item.objects.filter(
            teachers__in=[self.request.user.teacher]).filter(academicyears__in=[current_academic_year]).order_by(
            'name')
        exams = Exam.objects.filter(academic_year=current_academic_year).filter(item__in=items).order_by('-date_time')
        is_teacher = True
        return render(request, 'teacher/exams.html', context={'exams': exams, 'is_teacher': is_teacher})


class ExamRatingUpdate(TeacherTestMixin, UpdateView):
    """Logged teacher can update exam's ratings"""
    model = StudentExam
    fields = ['student', 'exam', 'rating', 'is_passed']
    template_name = 'teacher/exam_create.html'
    success_url = reverse_lazy('teacher:exams')

    def get_form(self, *args, **kwargs):
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

    def handle_no_permission(self):
        if TeacherTestMixin.is_teacher(self):
            return EmptyForm();
        else:
            return redirect(reverse('users:login'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_teacher'] = True
        return context


class StudentsYearView(SuperUserTestMixin, View):
    def get(self, request):
        current_academic_year = AcademicYear.objects.filter(
            name=self.request.session.get('current_academic_year')).first()
        students = Student.objects.filter(academic_years__in=[current_academic_year]).order_by('user__last_name')
        students_by_level = {}
        for student in students:
            level_number = student.level
            if level_number not in students_by_level:
                students_by_level[level_number] = {'level': student.level, 'students': []}
            students_by_level[level_number]['students'].append(student)

        # You can now pass the 'students_by_level' dictionary to the template
        return render(request, 'teacher/students.html', {'students_by_level': students_by_level})


class StudentDetailView(SuperUserTestMixin, View):
    def get(self, request, *args, **kwargs):
        current_academic_year = AcademicYear.objects.filter(
            name=self.request.session.get('current_academic_year')).first()
        student = Student.objects.get(pk=self.kwargs['pk'])
        exams = student.exams.filter(academic_year=current_academic_year)
        exams = StudentExam.objects.filter(student=student, exam__in=exams)
        return render(request, 'teacher/student.html', context={'student': student, 'exams': exams})


class PromoteView(SuperUserTestMixin, UpdateView):
    model = Student
    fields = ['level']
    template_name = 'teacher/student_promote.html'
    success_url = reverse_lazy('teacher:promote')


