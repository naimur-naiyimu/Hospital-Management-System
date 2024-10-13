from django.urls import path

from . import views

app_name = 'staff'

urlpatterns = [
    path('doctor/', views.doctor_list, name='doctor-list'),
    path('doctor/create/', views.doctor_create, name='doctor-create'),
    path('doctor/<int:pk>/', views.doctor_detail, name='doctor-detail'),
    path('doctor/<int:pk>/update/', views.doctor_update, name='doctor-update'),
    path('doctor/<int:pk>/delete/', views.doctor_delete, name='doctor-delete'),

    # staff 
    path('', views.staff_list, name='staff-list'),
    path('<int:pk>/', views.staff_detail, name='staff-detail'),
    path('create/', views.staff_create, name='staff-create'),
    path('<int:pk>/update/', views.staff_update, name='staff-update'),
    path('<int:pk>/delete/', views.staff_delete, name='staff-delete'),
]