from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views import View
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from config import settings
from teacher.models import Rating, Exam, StudentExam, Reunion
from .models import AcademicYear, Item
from django.views.generic import ListView, DetailView


# Create your views here.
def home(request):
    try:
        current_academic_year = AcademicYear.objects.filter(started_at__lt=datetime.today()).filter(
            finished_at__gt=datetime.today()).first()
        request.session['current_academic_year'] = current_academic_year.name
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


class ItemsView(View, LoginRequiredMixin):
    def get(self, request):
        is_student = request.session.get('is_student')
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
    template_name = 'student/reunion_list.html'

    def queryset(self):
        current_academic_year = AcademicYear.objects.filter(
            name=self.request.session.get('current_academic_year')).first()
        queryset = Reunion.objects.filter(academic_year=current_academic_year).filter(
            level=self.request.user.student.level)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super(ReunionsView, self).get_context_data(*args, **kwargs)
        context['is_student'] = self.request.session.get('is_student')
        return context

    context_object_name = 'reunions'


class ReunionDetailView(LoginRequiredMixin, DetailView):
    model = Reunion
    template_name = 'student/reunion_details.html'
    def get_context_data(self, *args, **kwargs):
        context = super(ReunionDetailView, self).get_context_data(*args, **kwargs)
        context['is_student'] = self.request.session.get('is_student')
        return context
    context_object_name = 'reunion'
