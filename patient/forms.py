from django import forms
from .models import Patient
from administrations.models import Bed 
class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Full Name'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control form-control-lg datepicker','type': 'date', 'placeholder': 'Date of Birth'}),
            'gender': forms.Select(attrs={'class': 'form-control form-control-lg'}),
            'blood_group': forms.Select(attrs={'class': 'form-control form-control-lg'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Contact Number'}),
            'address': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Address'}),
            'emergency_contact': forms.Select(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Emergency Contact'}),
            'admission_date': forms.DateTimeInput(attrs={'class': 'form-control form-control-lg datepicker','type':"datetime-local" , 'placeholder': 'Admission Date'}),
            'release_date': forms.DateTimeInput(attrs={'class': 'form-control form-control-lg datepicker','type':"datetime-local" ,  'placeholder': 'Release Date'}),
            'allocated_bed': forms.Select(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Allocated Bed'}),

            'emergency_full_name': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Full Name'}),
            'emergency_gender': forms.Select(attrs={'class': 'form-control form-control-lg'}),
            'emergency_contact_number': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Contact Number'}),
            'emergency_blood_group': forms.Select(attrs={'class': 'form-control form-control-lg'}),
            'emergency_address': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Address'}),
            'relation_with_patient': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Relation with Patient'}),
        }
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['allocated_bed'].queryset = Bed.objects.filter(is_occupied=False)
