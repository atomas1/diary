from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('', views.PasswordChange.as_view(), name='change_password'),
    path('academic-year/', views.ChooseAcademicYear.as_view(), name='change_academic_year'),
]
