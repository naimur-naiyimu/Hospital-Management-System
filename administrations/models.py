from django.db import models
from decimal import Decimal
# Create your models here.


class Appointment(models.Model):
    patient = models.ForeignKey(
        'patient.Patient', on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(
        'staff.Doctor', on_delete=models.CASCADE, related_name='doctor_appointments')
    appointment_date = models.DateTimeField()
    symptoms = models.TextField()
    status_choices = [('Scheduled', 'Scheduled'),
                      ('Completed', 'Completed'), ('Canceled', 'Canceled')]
    status = models.CharField(max_length=10, choices=status_choices)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Appointment for {self.patient.full_name} with Dr. {self.doctor.full_name} on {self.appointment_date}"


class Prescription(models.Model):
    patient = models.ForeignKey(
        'patient.Patient', on_delete=models.CASCADE, related_name='prescriptions')
    doctor = models.ForeignKey(
        'staff.Doctor', on_delete=models.CASCADE, related_name='doctor_prescriptions')
    issue_date = models.DateTimeField()
    next_appointment_date = models.DateTimeField(null=True, blank=True)
    medication = models.TextField(null=True, blank=True)
    dosage = models.TextField(null=True, blank=True)
    test = models.TextField(null=True, blank=True)
    instructions = models.TextField(null=True, blank=True)
    is_reviewed = models.BooleanField(default=False)

    def __str__(self):
        return f"Prescription for {self.patient.full_name} by Dr. {self.doctor.full_name} issued on {self.issue_date}"


class MedicalReport(models.Model):
    patient = models.ForeignKey(
        'patient.Patient', on_delete=models.CASCADE, related_name='medical_reports')
    test_date = models.DateTimeField(blank=True, null=True)
    delivery_date = models.DateTimeField(blank=True, null=True)
    test_name = models.CharField(max_length=100, blank=True, null=True)
    fee = models.PositiveIntegerField(null=True, blank=True)
    results = models.TextField(blank=True, null=True)
    report_file = models.FileField(blank=True, null=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Medical Report for {self.patient.full_name} - {self.test_name}"


class Ward(models.Model):
    department_name = models.CharField(max_length=100)
    head_of_department = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    ward_number = models.CharField(max_length=10)
    type_choices = [('General', 'General'), ('Semi-Private',
                                             'Semi-Private'), ('Private', 'Private')]
    type = models.CharField(max_length=15, choices=type_choices)
    fee = models.PositiveIntegerField(null=True, blank=True)
    capacity = models.PositiveIntegerField()
    occupancy = models.PositiveIntegerField(default=0)

    def available_beds(self):
        return self.capacity - self.occupancy

    def __str__(self):
        if self.available_beds() == 0:
            return f"Ward {self.ward_number} and Available bed is: N/A"
        else:
            return f"Ward {self.ward_number}"

    def save(self, *args, **kwargs):
        created = not self.pk  # Check if the ward is being created or updated
        super().save(*args, **kwargs)
        if created:
            # Automatically create bed instances based on the ward's capacity
            for i in range(1, self.capacity + 1):
                bed = Bed.objects.create(ward=self, bed_number=str(i))


class Bed(models.Model):
    ward = models.ForeignKey(
        Ward, on_delete=models.CASCADE, null=True, blank=True)
    bed_number = models.CharField(max_length=10)
    is_occupied = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"ward {self.ward} Bed {self.bed_number}"


class Invoice(models.Model):
    patient = models.ForeignKey('patient.Patient', on_delete=models.CASCADE)
    invoice_date = models.DateTimeField()
    appointment_fee = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    bed_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    admission_days = models.IntegerField(default=0)
    release_date = models.DateTimeField(blank=True, null=True)
    admission_date = models.DateTimeField(blank=True, null=True)
    MedicalReport_fee = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    Discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    Discount_flat = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    final_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    is_paid = models.BooleanField(default=False)

    appointments = models.ManyToManyField(
        Appointment, related_name='invoices', blank=True)
    medical_reports = models.ManyToManyField(
        MedicalReport, related_name='invoices', blank=True)

    custom_data = models.JSONField(default=dict)

    def calculate_appointment_fee(self):
        self.appointment_fee = sum(
            appointment.doctor.fees for appointment in self.appointments.all())
        return self.appointment_fee

    def calculate_bed_fee(self):
        if self.patient.is_paid is False and self.patient.allocated_bed and self.patient.allocated_bed.ward and self.patient.allocated_bed.ward.fee:
            self.admission_days = (self.patient.release_date - self.patient.admission_date).days if self.patient.admission_date else 0
            self.bed_fee = self.patient.allocated_bed.ward.fee * self.admission_days
        else:
            self.bed_fee = 0
        return self.bed_fee

    def calculate_medical_report_fee(self):
        self.MedicalReport_fee = sum(
            report.fee for report in self.medical_reports.all())
        return self.MedicalReport_fee

    def calculate_total_amount(self):
        custom_data_sum = sum(Decimal(value) for value in self.custom_data.values())
        self.total_amount = self.appointment_fee + self.bed_fee + self.MedicalReport_fee + custom_data_sum
        return self.total_amount

    def calculate_discount_amount(self):
        self.discount_amount = ((self.total_amount * self.Discount) / 100) + self.Discount_flat
        return self.discount_amount

    def calculate_amount(self):
        self.final_amount = self.total_amount - self.discount_amount
        return self.final_amount

    def save(self, *args, **kwargs):
        if not self.pk:
            # Save the instance for the first time to get an ID
            super().save(*args, **kwargs)

        else:
            super().save(*args, **kwargs)

        # Calculate other fields
        self.calculate_appointment_fee()
        self.calculate_bed_fee()
        self.calculate_medical_report_fee()
        self.calculate_total_amount()
        self.calculate_discount_amount()
        self.calculate_amount()

        # Save again to update the calculated fields
        super().save(update_fields=['appointment_fee', 'total_amount',
                                    'discount_amount', 'final_amount', 'MedicalReport_fee'])

    def __str__(self):
        return f"Invoice for {self.patient.full_name} - Invoice Date: {self.invoice_date}"
