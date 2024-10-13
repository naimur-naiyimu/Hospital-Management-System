from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from .forms import UserRegistrationForm, CustomAuthenticationForm
from patient.models import Patient
from staff.models import Doctor

class UserRegistrationView(View):
    template_name = 'register.html'
    form_class = UserRegistrationForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            return redirect('login')
        return render(request, self.template_name, {'form': form})

def CustomLoginView(request):
    if request.method == 'POST':
        mobile = request.POST['mobile']
        password = request.POST['password']
        user = authenticate(request, mobile=mobile, password=password)
        if user:
            login(request, user)
            if user.user_type == 0 or user.is_superuser:  # Admin & supperuser
                return redirect('dashboard')
            elif user.user_type == 1 : # Doctor
                try:
                    doctor = Doctor.objects.get(contact_number=user.mobile)
                    return redirect('staff:doctor-detail', pk=doctor.pk)
                except Doctor.DoesNotExist:
                    return redirect('staff:doctor-create')
            else:  # Patient
                try:
                    patient = Patient.objects.get(contact_number=user.mobile)
                    return redirect('patient:patient-detail', pk=patient.pk)
                except Patient.DoesNotExist:
                    return redirect('patient:patient-create')

        else:
            authentication_error = "Invalid credentials. Please check your mobile number and password."
            return render(request, 'login.html', {'authentication_error': authentication_error})

    return render(request, 'login.html')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')
