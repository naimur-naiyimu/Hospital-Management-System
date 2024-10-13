from django import forms
from .models import Appointment, Ward, Bed, Prescription, MedicalReport, Invoice
from patient.models import Patient
class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = '__all__'
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-control form-control-lg', "width":"100%",'id': 'id_patienta'}),
            'doctor': forms.Select(attrs={'class': 'form-control form-control-lg','id': 'id_doctor'}),
            'appointment_date': forms.DateTimeInput(attrs={'class': 'form-control form-control-lg', 'type': 'datetime-local'}),
            'symptoms': forms.Textarea(attrs={'class': 'form-control form-control-lg', 'rows': 5, 'cols': 100}),
            'status': forms.Select(attrs={'class': 'fform-control form-control-lg'}),
        }
class WardForm(forms.ModelForm):
    class Meta:
        model = Ward
        fields = '__all__'
        widgets = {
            'department_name': forms.TextInput(attrs={'class': 'form-control'}),
            'head_of_department': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control'}),
            'ward_number': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-select'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control'}),
            'occupancy': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class BedForm(forms.ModelForm):
    class Meta:
        pass
        # model = Bed
        # fields = '__all__' 
    patient = forms.ModelChoiceField(
        queryset=Patient.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select form-control-lg', 'id': 'id_patient'}),
        label='Select a Patient'
        )
    # class Meta:
    #     model = Bed
    #     fields = '__all__'
    #     widgets = {
    #         'patient': forms.Select(attrs={'class': 'form-select form-control-lg','id': 'id_patient'}),
    #         'ward': forms.Select(attrs={'class': 'form-select form-control-lg','id': 'id_ward'}),
    #     }

    # def __init__(self, *args, **kwargs):
    #     initial_ward = kwargs.pop('initial_ward', None)  # Get initial value from kwargs
    #     super().__init__(*args, **kwargs)
    #     if initial_ward:
    #         self.fields['ward'].initial = initial_ward 


class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields ='__all__'
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-control form-control-lg','id': 'id_patient'}),
            'doctor': forms.Select(attrs={'class': 'form-control form-control-lg','id': 'id_doctor'}),
            'issue_date': forms.DateTimeInput(attrs={'class': 'form-control form-control-lg', 'type': 'datetime-local'}),
            'next_appointment_date': forms.DateTimeInput(attrs={'class': 'form-control form-control-lg', 'type': 'datetime-local'}),
            'medication': forms.Textarea(attrs={ 'name':"medication", 'cols':"100" ,'rows':"3",'class': 'form-control'}),
            'dosage': forms.Textarea(attrs={'name':"dosage", 'cols':"100" ,'rows':"5",'class': 'form-control'}),
            'test': forms.Textarea(attrs={'name':"test", 'cols':"100" ,'rows':"5",'class': 'form-control'}),
            'instructions': forms.Textarea(attrs={'name':"instructions", 'cols':"100" ,'rows':"3",'class': 'form-control'}),
            # 'is_reviewed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class MedicalReportForm(forms.ModelForm):
    class Meta:
        model = MedicalReport
        fields = '__all__'
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-control-lg ','id': 'id_patientm'}),
            'test_date': forms.DateTimeInput(attrs={'class': 'form-control-lg', 'type': 'datetime-local'}),
            'delivery_date': forms.DateTimeInput(attrs={'class': 'form-control-lg', 'type': 'datetime-local'}),
            'test_name': forms.TextInput(attrs={'class': 'form-control'}),
            'fee': forms.NumberInput(attrs={'class': 'form-control'}),
            'results': forms.TextInput(attrs={'class': 'form-control'}),
            'report_file': forms.FileInput(attrs={'class': 'form-control-lg'}),
        }

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = [ 'Discount', 'is_paid','Discount_flat']

        widgets = {
            'Discount': forms.NumberInput(attrs={'class': 'form-control'}),
            'Discount_flat': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_paid': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
