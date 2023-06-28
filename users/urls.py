from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('', views.PasswordChange.as_view(), name='change_password'),
    path('academic-year/', views.ChooseAcademicYear.as_view(), name='change_academic_year'),
]
