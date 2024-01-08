from django.urls import path

from . import views

app_name = 'student'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('student/items/', views.ItemsView.as_view(), name='items_view'),
    path('student/reunions/', views.ReunionsView.as_view(), name='reunions_view'),
    path('student/reunion/<int:pk>/', views.ReunionDetailView.as_view(), name='reunion-detail'),

]