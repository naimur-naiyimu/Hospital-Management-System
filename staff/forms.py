from django import forms
from .models import Doctor, Staff

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = '__all__'
        widgets = {
        'full_name': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Full Name'}),
        'date_of_birth': forms.DateInput(attrs={'class': 'form-control form-control-lg datepicker', 'type': 'date', 'placeholder': 'Date of Birth'}),
        'gender': forms.Select(attrs={'class': 'form-control form-control-lg'}),
        'blood_group': forms.Select(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Blood Group'}),
        'contact_number': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Contact Number'}),
        'photo': forms.FileInput(attrs={'class': 'form-control form-control-lg'}),
        'specialization': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Specialization'}),
        'certificate': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Certificate'}),
        'fees': forms.NumberInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Fees'}),
        'salary': forms.NumberInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Salary'}),
        'address': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Address'}),
    }

class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = '__all__'
        widgets = {
        'full_name': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Full Name'}),
        'date_of_birth': forms.DateInput(attrs={'class': 'form-control form-control-lg datepicker', 'type': 'date', 'placeholder': 'Date of Birth'}),
        'gender': forms.Select(attrs={'class': 'form-control form-control-lg'}),
        'blood_group': forms.Select(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Blood Group'}),
        'contact_number': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Contact Number'}),
        'photo': forms.FileInput(attrs={'class': 'form-control form-control-lg'}),
        'salary': forms.NumberInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Salary'}),
        'address': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Address'}),
        'role': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Role'}),
        
    }