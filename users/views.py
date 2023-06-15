from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views import View
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect

from student.models import AcademicYear
from .forms import ChooseAcademicYearForm


class PasswordChange(LoginRequiredMixin, View):
    def post(self, request):
        form = PasswordChangeForm(request.user, request.POST)
        is_teacher = self.request.session.get('is_teacher')
        is_student = self.request.session.get('is_student')
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('users:change_password')
        else:
            messages.error(request, 'Please correct the error below.')
        return render(request, 'users/change_password.html', {
            'form': form,
            'is_teacher': is_teacher,
            'is_student':is_student
        })

    def get(self, request):
        form = PasswordChangeForm(request.user)
        is_teacher = self.request.session.get('is_teacher')
        is_student = self.request.session.get('is_student')

        return render(request, 'users/change_password.html', {
            'form': form,
            'is_teacher':is_teacher,
            'is_student':is_student
        })


class ChooseAcademicYear(LoginRequiredMixin, View):
    def post(self, request):
        form = ChooseAcademicYearForm(request.POST)
        if form.is_valid():
            chosen_academic_year = form.cleaned_data['current_academic_year']
            request.session['current_academic_year'] = chosen_academic_year.name
            return redirect('student:home')

    def get(self, request):
        form = ChooseAcademicYearForm(
            initial={'current_academic_year': AcademicYear.objects.all().order_by('-started_at').first()})
        is_teacher = self.request.session.get('is_teacher')
        is_student = self.request.session.get('is_student')
        return render(request, 'users/change_academic_year.html', {'form': form, 'is_teacher':is_teacher, 'is_student': is_student})

