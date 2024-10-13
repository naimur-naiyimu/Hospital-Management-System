from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from coreapp.decorator import allowed_users
from .models import Appointment, Ward, Bed, Prescription, MedicalReport, Invoice
from patient.models import Patient
from .forms import AppointmentForm, WardForm, BedForm, PrescriptionForm, MedicalReportForm, InvoiceForm
from django.db.models import Q
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string
from weasyprint import HTML, CSS
from django.contrib import messages
import json
from django.core.paginator import Paginator
from coreapp.pagination import paginate

@login_required(login_url='login')
@allowed_users(allowed_roles=[0,1])
def appointment_list(request):
    search_query = request.GET.get('search')
    if search_query:
        appointments = Appointment.objects.filter(
            Q(patient__full_name__icontains=search_query) |
            Q(patient__contact_number__icontains=search_query) |
            Q(doctor__full_name__icontains=search_query) |
            Q(appointment_date__icontains=search_query) |
            Q(status__icontains=search_query)
        ).order_by('-id')
    else:
        appointments = Appointment.objects.all().order_by('-id')
    appointments = paginate(request, appointments, 10)

    return render(request, 'appointment_list.html', {'appointments': appointments})

@login_required(login_url='login')
@allowed_users(allowed_roles=[0,2])
def appointment_create(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('administrations:appointment-list')
    else:
        form = AppointmentForm()
    return render(request, 'appointment_form.html', {'form': form, 'update': False})

@login_required(login_url='login')
@allowed_users(allowed_roles=[0,1,2])
def appointment_detail(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    return render(request, 'appointment_detail.html', {'appointment': appointment})

@login_required(login_url='login')
@allowed_users(allowed_roles=[0])
def appointment_update(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('administrations:appointment-detail', pk=appointment.pk)
    else:
        form = AppointmentForm(instance=appointment)
    return render(request, 'appointment_form.html', {'form': form, 'update': True, 'appointment': appointment})

@login_required(login_url='login')
@allowed_users(allowed_roles=[0])
def appointment_delete(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        appointment.delete()
        return redirect('administrations:appointment-list')
    return render(request, 'appointment_confirm_delete.html', {'appointment': appointment})


# ward CRUD
@login_required(login_url='login')
@allowed_users(allowed_roles=[0])
def ward_list(request):
    wards = Ward.objects.all()
    return render(request, 'ward_list.html', {'wards': wards})

@login_required(login_url='login')
@allowed_users(allowed_roles=[0])
def ward_detail(request, pk):
    ward = Ward.objects.get(pk=pk)
    return render(request, 'ward_detail.html', {'ward': ward})

@login_required(login_url='login')
@allowed_users(allowed_roles=[0])
def ward_create(request):
    if request.method == 'POST':
        form = WardForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('administrations:ward_list')
    else:
        form = WardForm()
    return render(request, 'ward_form.html', {'form': form})

@login_required(login_url='login')
@allowed_users(allowed_roles=[0])
def ward_update(request, pk):
    ward = Ward.objects.get(pk=pk)
    if request.method == 'POST':
        form = WardForm(request.POST, instance=ward)
        if form.is_valid():
            form.save()
            return redirect('administrations:ward_list')
    else:
        form = WardForm(instance=ward)
    return render(request, 'ward_form.html', {'form': form})

@login_required(login_url='login')
@allowed_users(allowed_roles=[0])
def ward_delete(request, pk):
    ward = Ward.objects.get(pk=pk)
    if request.method == 'POST':
        ward.delete()
        return redirect('administrations:ward_list')
    return render(request, 'ward_confirm_delete.html', {'ward': ward})

# beds

@login_required(login_url='login')
@allowed_users(allowed_roles=[0])
def bed_list(request):
    wards = Ward.objects.all()
    beds = Bed.objects.all()
    return render(request, 'bed_list.html', {'beds': beds,'wards': wards})

@login_required(login_url='login')
@allowed_users(allowed_roles=[0])
def bed_detail(request, pk):
    bed = get_object_or_404(Bed, pk=pk)
    patient = Patient.objects.filter(release_date=None, allocated_bed=bed.pk).first()
    print(patient)
    
    return render(request, 'bed_detail.html', {'bed': bed, 'patient': patient})

@login_required(login_url='login')
@allowed_users(allowed_roles=[0])
def add_patient(request, pk):
    bed = get_object_or_404(Bed, pk=pk)
    if bed.is_occupied:
        patient = Patient.objects.filter(release_date=None, allocated_bed=bed.pk).first()
        print(patient)
        patient.release_date = timezone.now()
        patient.save()
        bed.is_occupied = False
        bed.save()
        return redirect('administrations:bed_list')
    if request.method == 'POST':
        patient_id = request.POST.get('patient')
        patient = get_object_or_404(Patient, pk=patient_id)
        patient.allocated_bed = bed
        patient.admission_date = timezone.now()
        patient.release_date = None
        patient.save()
        bed.is_occupied = True
        bed.save()

        return redirect('administrations:bed_list')

    patients = Patient.objects.all()
    return render(request, 'add_patient.html', {'bed':bed, 'patients':patients})


# rescription
@login_required(login_url='login')
@allowed_users(allowed_roles=[0,1])
def prescription_list(request):
    search_query = request.GET.get('search')
    if search_query:
        prescriptions = Prescription.objects.filter(
            Q(patient__full_name__icontains=search_query) |
            Q(doctor__full_name__icontains=search_query) |
            Q(issue_date__icontains=search_query) |
            Q(next_appointment_date__icontains=search_query)
        )
    else:
        prescriptions = Prescription.objects.all()

    prescriptions = paginate(request, prescriptions, 10)
    return render(request, 'prescription_list.html', {'prescriptions': prescriptions})

@login_required(login_url='login')
@allowed_users(allowed_roles=[0,1])
def add_prescription(request):
    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.save()
            return redirect('administrations:prescription-list')
    else:
        form = PrescriptionForm()
    return render(request, 'add_prescription.html', {'form': form})

@login_required(login_url='login')
@allowed_users(allowed_roles=[0,1,2])
def prescription_detail(request, prescription_id):
    prescription = get_object_or_404(Prescription, pk=prescription_id)
    return render(request, 'prescription_detail.html', {'prescription': prescription})

@login_required(login_url='login')
@allowed_users(allowed_roles=[0,1])
def edit_prescription(request,  prescription_id):
    prescription = get_object_or_404(Prescription, pk=prescription_id)
    if request.method == 'POST':
        form = PrescriptionForm(request.POST, instance=prescription)
        if form.is_valid():
            form.save()
            return redirect('administrations:prescription-detail',  prescription_id=prescription_id)
    else:
        form = PrescriptionForm(instance=prescription)
    return render(request, 'edit_prescription.html', {'prescription': prescription, 'form': form})

@login_required(login_url='login')
@allowed_users(allowed_roles=[0])
def delete_prescription(request, prescription_id):
    prescription = get_object_or_404(Prescription, pk=prescription_id)
    if request.method == 'POST':
        prescription.delete()
        return redirect('administrations:prescription-list')
    return render(request, 'delete_prescription.html', {'prescription': prescription})


# medical report CRUD
@login_required(login_url='login')
@allowed_users(allowed_roles=[0,2])
def medical_report_list(request):
    search_query = request.GET.get('search')
    if search_query:
        medical_reports = MedicalReport.objects.filter(
            Q(patient__full_name__icontains=search_query) |
            Q(patient__contact_number__icontains=search_query) |
            Q(test_date__icontains=search_query) |
            Q(test_name__icontains=search_query) |
            Q(delivery_date__icontains=search_query)
        ).order_by('-id')
    else:
        medical_reports = MedicalReport.objects.all().order_by('-id')
    medical_reports = paginate(request, medical_reports, 10)
    return render(request, 'medical_report_list.html', {'medical_reports': medical_reports})

@login_required(login_url='login')
@allowed_users(allowed_roles=[0,1])
def add_medical_report(request):
    if request.method == 'POST':
        form = MedicalReportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('administrations:medical-report-list')
    else:
        form = MedicalReportForm()
    return render(request, 'add_medical_report.html', {'form': form})

@login_required(login_url='login')
@allowed_users(allowed_roles=[0,1,2])
def medical_report_detail(request, report_id):
    medical_report = get_object_or_404(MedicalReport, pk=report_id)
    return render(request, 'medical_report_detail.html', {'medical_report': medical_report})

@login_required(login_url='login')
@allowed_users(allowed_roles=[0,1])
def edit_medical_report(request, report_id):
    medical_report = get_object_or_404(MedicalReport, pk=report_id)
    if request.method == 'POST':
        form = MedicalReportForm(request.POST, instance=medical_report)
        if form.is_valid():
            form.save()
            return redirect('administrations:medical-report-list')
    else:
        form = MedicalReportForm(instance=medical_report)
    return render(request, 'edit_medical_report.html', {'form': form, 'medical_report': medical_report})


@login_required(login_url='login')
@allowed_users(allowed_roles=[0])
def delete_medical_report(request, report_id):
    medical_report = get_object_or_404(MedicalReport, pk=report_id)
    if request.method == 'POST':
        medical_report.delete()
        return redirect('administrations:medical-report-list')
    return render(request, 'delete_medical_report.html', {'medical_report': medical_report})

# incoice

@login_required(login_url='login')
@allowed_users(allowed_roles=[0])
def create_invoice(request, pk):
    try:
        patient = get_object_or_404(Patient, pk=pk)
        appointments = Appointment.objects.filter(patient=patient, is_paid=False).order_by('-pk')
        medical_reports = MedicalReport.objects.filter(patient=patient, is_paid=False).order_by('-pk')

        # if appointments or patient.allocated_bed.is_paid == False or medical_reports:
        invoice = Invoice.objects.create(
            patient=patient,
            invoice_date=timezone.now(),
        )
        invoice.appointments.set(appointments)
        invoice.medical_reports.set(medical_reports)
        invoice.save()

        return redirect('administrations:update-invoice', invoice_id=invoice.id)
        # else:
        #     return HttpResponse("No unpaid appointments, beds, or medical reports found for this patient.")

    except ObjectDoesNotExist:
        return redirect('patient:patient-list')

@login_required(login_url='login')
@allowed_users(allowed_roles=[0,2])
def select_patient_for_invoice(request):
    patients = Patient.objects.all()

    if request.method == 'POST':
        patient_id = request.POST.get('patient')
        patient = get_object_or_404(Patient, pk=patient_id)

        try:
            return create_invoice(request, patient.pk)  # Return the response from create_invoice
        except TypeError:
            pass
    return render(request, 'select_patient_for_invoice.html', {'patients': patients})

@login_required(login_url='login')
@allowed_users(allowed_roles=[0,2])
def customize_invoice(request):
    patients = Patient.objects.all()

    if request.method == 'POST':
        patient_id = request.POST.get('patient')
        patient = get_object_or_404(Patient, pk=patient_id)
        descriptions = request.POST.getlist('description')
        amounts = request.POST.getlist('amount')
        appointments = Appointment.objects.filter(patient=patient, is_paid=False).order_by('-pk')
        medical_reports = MedicalReport.objects.filter(patient=patient, is_paid=False).order_by('-pk')

        # if appointments or patient.allocated_bed.is_paid == False or medical_reports or descriptions:
        invoice = Invoice.objects.create(
            patient=patient,
            invoice_date=timezone.now(),
        )
        invoice.appointments.set(appointments)
        invoice.medical_reports.set(medical_reports)
        invoice.save()

        return redirect('administrations:update-invoice', invoice_id=invoice.id)
        # else:
        #     return HttpResponse("No unpaid appointments, beds, or medical reports found for this patient.")
    return render(request, 'customize_invoice.html', {'patients': patients})

@login_required(login_url='login')
@allowed_users(allowed_roles=[0])
def invoice_list(request):
    invoices = Invoice.objects.all().order_by('-pk')
    invoices = paginate(request, invoices, 2)
    return render(request, 'invoice_list.html', {'invoices': invoices})

@login_required(login_url='login')
@allowed_users(allowed_roles=[0,2])
def invoice_detail(request, invoice_id):
    try:
        invoice = get_object_or_404(Invoice, pk=invoice_id)
        return render(request, 'invoice_detail.html', {
            'invoice': invoice,
        })
    except Invoice.DoesNotExist:
        return HttpResponse("No invoice available with this ID.")


@login_required(login_url='login')
@allowed_users(allowed_roles=[0]) 
def update_invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    patient = get_object_or_404(Patient, pk=invoice.patient.pk)
    medical_reports = MedicalReport.objects.filter(patient=patient, is_paid=False).order_by('-pk')
    appointments = Appointment.objects.filter(patient=patient, is_paid=False)

    if request.method == 'POST':
        form = InvoiceForm(request.POST, instance=invoice)
        if form.is_valid():
            form.save()
            new_payment_status = request.POST.get('is_paid')
            if new_payment_status == 'paid':
                invoice.is_paid = True
                if patient:
                    patient.is_paid = True
                    patient.save()
                for appointment in appointments:
                    appointment.is_paid = True
                    appointment.save()
                for report in medical_reports:
                    report.is_paid = True
                    report.save()
            elif new_payment_status == 'unpaid':
                invoice.is_paid = False
                if patient:
                    patient.is_paid = False
                    patient.save()
                for appointment in appointments:
                    appointment.is_paid = False
                    appointment.save()
                for report in medical_reports:
                    report.is_paid = False
                    report.save()

            descriptions = request.POST.getlist('description[]')
            amounts = request.POST.getlist('amount[]')
            
            # Filter out empty values
            descriptions = [desc for desc in descriptions if desc.strip()]
            amounts = [amount for amount in amounts if amount.strip()]
            print(f"description: {descriptions}")
            print(f"Amount: {amounts}")

            # Retrieve the existing custom data
            existing_custom_data = invoice.custom_data

            # Create a dictionary for the new data
            new_custom_data = {}
            for i in range(len(descriptions)):
                description = descriptions[i]
                amount = amounts[i]
                new_custom_data[description] = amount

            # Update the existing custom data with the new data
            existing_custom_data.update(new_custom_data)

            # Set the custom_data field with the updated dictionary
            invoice.custom_data = existing_custom_data
            invoice.save()
            return redirect('administrations:invoice-detail', invoice_id=invoice.id )
        else:
            print(form.errors)
    else:
        form = InvoiceForm(instance=invoice)

    return render(request, 'invoice_update.html', {
        'form': form,
        'invoice': invoice,
    })

@login_required(login_url='login')
@allowed_users(allowed_roles=[0])
def invoice_delete(request, invoice_id):
    invoice = get_object_or_404(Invoice, pk=invoice_id)
    if request.method == 'POST':
        invoice.delete()
        return redirect('administrations:invoice_list')

@login_required(login_url='login')
@allowed_users(allowed_roles=[0,2]) 
def print_invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)

    return render(request, 'invoice_print.html', context = {'invoice': invoice})

@login_required(login_url='login')
@allowed_users(allowed_roles=[0,2]) 
def generate_pdf(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)

    context = {
        'invoice': invoice,
    }
    # html_content = template.render(context)
    html_content = render_to_string('invoice_pdf.html',context)

    # Create a PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{invoice_id}.pdf"'

    # Generate the PDF using weasyprint
    HTML(string=html_content).write_pdf(response,stylesheets=[CSS(string='@page { size: letter portrait; margin: 1cm }')])

    return response