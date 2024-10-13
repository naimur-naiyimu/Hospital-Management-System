from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from coreapp.decorator import allowed_users
from .models import Patient
from .forms import PatientForm
from administrations.models import Appointment, Prescription, MedicalReport, Bed
from django.db.models import Q
from coreapp.models import User
from coreapp.pagination import paginate

@login_required(login_url='login')
@allowed_users(allowed_roles=[0,1])
def patient_list(request):
    search_query = request.GET.get('search')
    if search_query:
        patients = Patient.objects.filter(
            Q(full_name__icontains=search_query) |
            Q(gender__icontains=search_query) |
            Q(blood_group__icontains=search_query) |
            Q(contact_number__icontains=search_query) |
            Q(emergency_contact__full_name__icontains=search_query)
        ).order_by('-pk')
    else:
        patients = Patient.objects.all().order_by('-pk')

    patients = paginate(request, patients, 10)
    return render(request, 'patient_list.html', {'patients': patients})


@login_required(login_url='login')
@allowed_users(allowed_roles=[0,1,2])
def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    prescriptions = Prescription.objects.filter(patient=patient).order_by('-pk')
    medical_reports = MedicalReport.objects.filter(patient=patient).order_by('-pk')
    appointments = Appointment.objects.filter(patient=patient).order_by('-pk')
    beds = Bed.objects.filter(patient=patient)
    return render(request, 'patient_detail.html', {
        'patient': patient,
        'prescriptions': prescriptions,
        'medical_reports': medical_reports,
        'appointments':appointments,
        "beds":beds,
    })

@login_required(login_url='login')
@allowed_users(allowed_roles=[0,2])
def patient_create(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save()
            if request.user.user_type == 2:
                pk=patient.pk
                user = User.objects.get(id = request.user.id)
                user.patient__id = pk
                user.save()
            else:
                user = User.objects.create(
                    user_type = 2,
                    patient = patient,
                    name = patient.full_name,
                    mobile = patient.contact_number,
                    gender = patient.gender,
                )
                user.set_password (patient.contact_number)
                user.save()
            return redirect('patient:patient-detail',pk=patient.pk)
    elif request.user.user_type == 2:
        initial_data = {
            'full_name': request.user.name,
            'contact_number': request.user.mobile,
            'gender': request.user.gender,
        }
        
        form = PatientForm(initial=initial_data)
    else:
        form = PatientForm()
    return render(request, 'patient_form.html', {'form': form, 'update': False})


@login_required(login_url='login')
@allowed_users(allowed_roles=[0,2])
def patient_update(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('patient:patient-detail', pk=patient.pk)
    else:
        form = PatientForm(instance=patient)
    return render(request, 'patient_form.html', {'form': form, 'update': True, 'patient': patient})

@login_required(login_url='login')
@allowed_users(allowed_roles=[0])
def patient_delete(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        patient.delete()
        return redirect('patient:patient-list')
    return render(request, 'patient_confirm_delete.html', {'patient': patient})
