from django.urls import path
from . import views

app_name = 'administrations'

urlpatterns =[
    path('appointment/', views.appointment_list, name='appointment-list'),
    path('appointment/create/', views.appointment_create, name='appointment-create'),
    path('appointment/<int:pk>/', views.appointment_detail, name='appointment-detail'),
    path('appointment/<int:pk>/update/', views.appointment_update, name='appointment-update'),
    path('appointment/<int:pk>/delete/', views.appointment_delete, name='appointment-delete'),

# ward
    path('ward/', views.ward_list, name='ward_list'),
    path('ward/<int:pk>/', views.ward_detail, name='ward_detail'),
    path('ward/create/', views.ward_create, name='ward_create'),
    path('ward/<int:pk>/update/', views.ward_update, name='ward_update'),
    path('ward/<int:pk>/delete/', views.ward_delete, name='ward_delete'),
# beds
    path('bed/', views.bed_list, name='bed_list'),
    path('bed/<int:pk>/', views.bed_detail, name='bed_detail'),
    path('add-patient/<int:pk>/', views.add_patient, name='add-patient'),
#  pre
    path('prescriptions/', views.prescription_list, name='prescription-list'),
    path('prescriptions/add/', views.add_prescription, name='add-prescription'),
    path('prescriptions/<int:prescription_id>/', views.prescription_detail, name='prescription-detail'),
    path('pprescriptions/<int:prescription_id>/edit/', views.edit_prescription, name='edit-prescription'),
    path('prescriptions/<int:prescription_id>/delete/', views.delete_prescription, name='delete-prescription'),

    # Medical Report URLs
    path('medical-reports/', views.medical_report_list, name='medical-report-list'),
    path('medical-reports/add/', views.add_medical_report, name='add-medical-report'),
    path('medical-reports/<int:report_id>/', views.medical_report_detail, name='medical-report-detail'),
    path('medical-reports/<int:report_id>/edit/', views.edit_medical_report, name='edit-medical-report'),
    path('medical-reports/<int:report_id>/delete/', views.delete_medical_report, name='delete-medical-report'),

    # invoice
    path('create-invoice/<int:pk>/', views.create_invoice, name='create_invoice'),
    path('invoice-list/', views.invoice_list, name='invoice_list'),
    path('invoice/<int:invoice_id>/detail', views.invoice_detail, name='invoice-detail'),
    path('select-patient-for-invoice/', views.select_patient_for_invoice, name='select-patient-for-invoice'),
    path('customize-invoice/', views.customize_invoice, name='customize-invoice'),
    path('invoice/<int:invoice_id>/update/', views.update_invoice, name='update-invoice'),
    path('invoice/<int:invoice_id>/invoice-print/', views.print_invoice, name='invoice-print'),
    path('invoice/<int:invoice_id>/generate-pdf/', views.generate_pdf, name='generate-pdf'),
    path('invoice/delete/<int:invoice_id>/', views.invoice_delete, name='invoice-delete'),

]