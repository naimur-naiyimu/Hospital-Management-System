from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from staff.models import Doctor,Staff
from patient.models import Patient
from administrations.models import Ward, Appointment, Prescription
from staff.forms import DoctorForm,StaffForm
from django.db.models import Q
from coreapp.decorator import allowed_users
from coreapp.models import User
from coreapp.pagination import paginate

@login_required(login_url='login')
@allowed_users(allowed_roles=[0])
def dashboard(request): 
    doctors = Doctor.objects.all()
    patients = Patient.objects.all()
    wards = Ward.objects.all()
    appointments = Appointment.objects.all()
    staffs = Staff.objects.all()
    prescriptions = Prescription.objects.all()

    context = {
        'doctors_count': doctors.count(),
        'patients_count': patients.count(),
        'wards_count': wards.count(),
        'appointments_count': appointments.count(),
        'staffs_count':staffs.count(),
        'prescriptions_count': prescriptions.count(),
    }

    return render(request, 'dashboard.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=[0])
def doctor_list(request):
    search_query = request.GET.get('search')
    if search_query:
        doctors = Doctor.objects.filter(
            Q(full_name__icontains=search_query) |
            Q(gender__icontains=search_query) |
            Q(blood_group__icontains=search_query) |
            Q(contact_number__icontains=search_query) |
            Q(specialization__icontains=search_query)|
            Q(fees__icontains=search_query)
        ).order_by('-pk')
    else:
        doctors = Doctor.objects.all().order_by('-pk')
    doctors = paginate(request, doctors, 10)
    return render(request, 'doctor_list.html', {'doctors': doctors})

@login_required(login_url='login')
@allowed_users(allowed_roles=[0,1])
def doctor_create(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST, request.FILES)
        if form.is_valid():
            doctor = form.save()
            if request.user.user_type == 1:
                user = User.objects.get(id = request.user.id)
                user.doctor__id = doctor.pk
                user.save()
            else:
                user = User.objects.create(
                    user_type = 1,
                    doctor = doctor,
                    name = doctor.full_name,
                    mobile = doctor.contact_number,
                    gender = doctor.gender,
                )
                user.set_password (doctor.contact_number)
                user.save()
            return redirect('staff:doctor-detail', pk=doctor.pk)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"Error in {field}: {error}")
    elif request.user.user_type == 1:
        initial_data = {
            'full_name': request.user.name,
            'contact_number': request.user.mobile,
            'gender': request.user.gender,
        }
        form = DoctorForm(initial=initial_data)
    else:
        form = DoctorForm()
    return render(request, 'doctor_form.html', {'form': form, 'update': False})

@login_required(login_url='login')
@allowed_users(allowed_roles=[0,1])
def doctor_detail(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    prescriptions = Prescription.objects.filter(doctor=doctor).order_by('-pk')
    appointments = Appointment.objects.filter(doctor=doctor).order_by('-pk')
    return render(request, 'doctor_detail.html', {
        'doctor': doctor,
        'prescriptions': prescriptions,
        'appointments':appointments,
    })

@login_required(login_url='login')
@allowed_users(allowed_roles=[0,1])
def doctor_update(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    form = DoctorForm(request.POST, request.FILES, instance=doctor)
    if form.is_valid():
        if 'photo' in request.FILES:
            doctor.photo = request.FILES['photo']
        form.save()
        return redirect('staff:doctor-detail', pk=doctor.pk)
    else:
        form = DoctorForm(instance=doctor)
    return render(request, 'doctor_form.html', {'form': form, 'update': True, 'doctor': doctor})

@login_required(login_url='login')
@allowed_users(allowed_roles=[0])
def doctor_delete(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        doctor.delete()
        return redirect('staff:doctor-list')
    return render(request, 'doctor_confirm_delete.html', {'doctor': doctor})

'''Staff crud operations '''

@login_required(login_url='login')
@allowed_users(allowed_roles=[0])
def staff_list(request):
    search_query = request.GET.get('search')
    if search_query:
        doctors = Doctor.objects.filter(
            Q(full_name__icontains=search_query) |
            Q(gender__icontains=search_query) |
            Q(blood_group__icontains=search_query) |
            Q(contact_number__icontains=search_query) |
            Q(role__icontains=search_query)|
            Q(salary__icontains=search_query)
        ).order_by('-pk')
    else:
        staffs = Staff.objects.all().order_by('-pk')
    staffs = paginate(request, staffs, 10)
    return render(request, 'staff_list.html', {'staffs': staffs})

@login_required(login_url='login')
@allowed_users(allowed_roles=[0])
def staff_detail(request, pk): 
    staff = get_object_or_404(Staff, pk=pk)
    return render(request, 'staff_detail.html', {'staff': staff})

@login_required(login_url='login')
@allowed_users(allowed_roles=[0])
def staff_create(request):
    if request.method == 'POST':
        form = StaffForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('staff:staff-list')
    else:
        form = StaffForm()
    return render(request, 'staff_form.html', {'form': form, 'update': False})

@login_required(login_url='login')
@allowed_users(allowed_roles=[0])
def staff_update(request, pk):
    staff = get_object_or_404(Staff, pk=pk)
    form = StaffForm(request.POST, request.FILES, instance=staff)
    if form.is_valid():
        if 'photo' in request.FILES:
            staff.photo = request.FILES['photo']
        form.save()
        return redirect('staff:staff-detail', pk=staff.pk)
    else:
        form = StaffForm(instance=staff)
    return render(request, 'staff_form.html', {'form': form,'update': True, 'staff': staff})

@login_required(login_url='login')
@allowed_users(allowed_roles=[0])
def staff_delete(request, pk):
    staff = get_object_or_404(Staff, pk=pk)
    if request.method == 'POST':
        staff.delete()
        return redirect('staff:staff-list')
    return render(request, 'staff_confirm_delete.html', {'staff': staff})
