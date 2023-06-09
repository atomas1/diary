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
]