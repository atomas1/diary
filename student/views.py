from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views import View
from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings

from teacher.models import Rating, Exam, StudentExam, Reunion, Teacher
from utlis import TeacherTestMixin, StudentTestMixin
from .models import AcademicYear, Item


# Create your views here.
class HomeView(StudentTestMixin, View):
    """Default view for all project. It redirects to correct view after successfull login """

    def get(self, request):
        current_academic_year = AcademicYear.objects.all().order_by('-started_at').first()
        if current_academic_year:
            request.session['current_academic_year'] = current_academic_year.name
        else:
            request.session['current_academic_year'] = "No academic year selected"
        return redirect(reverse('student:items_view'))

    def handle_no_permission(self):
        if TeacherTestMixin.is_teacher(self):
            return redirect(reverse('teacher:home'))
        elif self.request.user.is_superuser:
            return redirect(reverse('teacher:promote'))
        else:
            return redirect(reverse('users:login'))


class ItemsView(StudentTestMixin, View):
    """Items of logged student in chosen academic year"""

    def get(self, request):
        # check if user is a student, if not redirect him to login page
        current_academic_year = AcademicYear.objects.filter(name=request.session.get('current_academic_year')).first()
        items = Item.objects.filter(
            Q(academicyears__in=[current_academic_year]) & Q(students__in=[request.user.student])).order_by('name')
        ratings = Rating.objects.filter(student=request.user.student)
        exams = Exam.objects.filter(students__in=[request.user.student]).filter(academic_year=current_academic_year)
        ratings_exams = StudentExam.objects.filter(student=request.user.student)
        return render(request, 'student/home.html',
                      context={'ratings': ratings, 'items': items, 'exams': exams, 'ratings_exams': ratings_exams,
                               'is_student': True})


class ReunionsView(StudentTestMixin, ListView):
    """reunions in current academic year for logged students"""
    template_name = 'student/reunion_list.html'

    def queryset(self):
        current_academic_year = AcademicYear.objects.filter(
            name=self.request.session.get('current_academic_year')).first()
        queryset = Reunion.objects.filter(academic_year=current_academic_year).filter(
            level=self.request.user.student.level)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['is_student'] = True
        return context

    context_object_name = 'reunions'


class ReunionDetailView(StudentTestMixin, DetailView):
    """Details of specific reunion"""
    model = Reunion
    template_name = 'student/reunion_details.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['is_student'] = True
        return context

    context_object_name = 'reunion'
