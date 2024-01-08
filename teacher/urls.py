from django.urls import path

from . import views

app_name = 'teacher'

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('rating/', views.RatingCreateView.as_view(), name='rating-create'),
    path('lesson/', views.LessonCreateView.as_view(), name='lesson-create'),
    path('lessons/', views.TeacherLessonsView.as_view(), name='lessons'),
    path('rating/<int:pk>/', views.RatingUpdateView.as_view(), name='rating-update'),
    path('lesson/<int:pk>/', views.LessonUpdateView.as_view(), name='lesson-update'),
    path('exam/<int:pk>/', views.ExamUpdateView.as_view(), name='exam-update'),
    path('exam/', views.ExamCreateView.as_view(), name='exam-create'),
    path('promote/', views.StudentsYearView.as_view(), name='promote'),
    path('student-details/<int:pk>/', views.StudentDetailView.as_view(), name='student-details'),
    path('exams/', views.TeacherExamsView.as_view(), name='exams'),
    path('exam/rating/<int:pk>/', views.ExamRatingUpdate.as_view(), name='exam-rating-update'),
    path('student/promote/<int:pk>/', views.PromoteView.as_view(), name='student-promote'),
]