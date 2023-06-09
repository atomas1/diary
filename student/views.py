from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views import View
from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings

from teacher.models import Rating, Exam, StudentExam, Reunion
from .models import AcademicYear, Item


# Create your views here.
def home(request):
    """Default view for all project. It redirects to correct view after successfull login """
    if not request.user.is_authenticated:
        return redirect(settings.LOGIN_URL)
    try:
        current_academic_year = AcademicYear.objects.all().order_by('-started_at').first()
        if current_academic_year:
            request.session['current_academic_year'] = current_academic_year.name
        else:
            request.session['current_academic_year'] = "No academic year selected"
        is_student = request.user.student.level
        request.session['is_student'] = True
        request.session['is_teacher'] = False
        return redirect(reverse('student:items_view'))

    except AttributeError:
        try:
            is_teacher = request.user.teacher.degree
            request.session['is_student'] = False
            request.session['is_teacher'] = True
            return redirect(reverse('teacher:home'))
        except AttributeError:
            return redirect(reverse(settings.LOGIN_URL))


class ItemsView(LoginRequiredMixin, View):
    """Items of logged student in chosen academic year"""

    def get(self, request):
        # check if user is a student, if not redirect him to login page
        is_student = request.session.get('is_student')
        if not is_student:
            return redirect(settings.LOGIN_URL)
        current_academic_year = AcademicYear.objects.filter(name=request.session.get('current_academic_year')).first()
        items = Item.objects.filter(
            Q(academicyears__in=[current_academic_year]) & Q(students__in=[request.user.student])).order_by('name')
        ratings = Rating.objects.filter(student=request.user.student)
        exams = Exam.objects.filter(students__in=[request.user.student]).filter(academic_year=current_academic_year)
        ratings_exams = StudentExam.objects.filter(student=request.user.student)
        return render(request, 'student/home.html',
                      context={'ratings': ratings, 'items': items, 'exams': exams, 'ratings_exams': ratings_exams,
                               'is_student': is_student})


class ReunionsView(LoginRequiredMixin, ListView):
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
        context['is_student'] = self.request.session.get('is_student')
        return context

    context_object_name = 'reunions'


class ReunionDetailView(LoginRequiredMixin, DetailView):
    """Details of specific reunion"""
    model = Reunion
    template_name = 'student/reunion_details.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['is_student'] = self.request.session.get('is_student')
        return context

    context_object_name = 'reunion'
