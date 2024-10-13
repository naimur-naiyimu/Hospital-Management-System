from django.urls import path
from . import views

app_name = 'patient'

urlpatterns = [
    path('', views.patient_list, name='patient-list'),
    path('create/', views.patient_create, name='patient-create'),
    path('<int:pk>/', views.patient_detail, name='patient-detail'),
    path('<int:pk>/update/', views.patient_update, name='patient-update'),
    path('<int:pk>/delete/', views.patient_delete, name='patient-delete'),
]
