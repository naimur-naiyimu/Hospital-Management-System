from django.db import models
from administrations.models import Bed, Prescription, MedicalReport, Appointment
from django.utils import timezone
# Create your models here.

# Choices for gender field
GENDER_CHOICES = [
    (0, 'Male'),
    (1, 'Female'),
    (2, 'Other'),
]

# Choices for blood_group field
BLOOD_GROUP_CHOICES = [
    ('A+', 'A+'),
    ('A-', 'A-'),
    ('B+', 'B+'),
    ('B-', 'B-'),
    ('AB+', 'AB+'),
    ('AB-', 'AB-'),
    ('O+', 'O+'),
    ('O-', 'O-'),
]

class Patient(models.Model):
    full_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.SmallIntegerField(choices=GENDER_CHOICES, default=1)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES, default='A+')
    address = models.TextField()
    contact_number = models.CharField(unique=True, max_length=20)

    admission_date = models.DateTimeField(null=True, blank=True)
    release_date = models.DateTimeField(null=True, blank=True)
    allocated_bed = models.ForeignKey(Bed, on_delete=models.SET_NULL, null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    
    relation_with_patient = models.CharField(max_length=100,null=True, blank=True)
    emergency_full_name = models.CharField(max_length=100,null=True, blank=True)
    emergency_gender =models.SmallIntegerField(choices=GENDER_CHOICES, default=0)
    emergency_blood_group = models.CharField(max_length=3,null=True, blank=True, choices=BLOOD_GROUP_CHOICES)
    emergency_address = models.TextField(null=True, blank=True)
    emergency_contact_number = models.CharField(max_length=15,null=True, blank=True)

    def __str__(self):
        return self.full_name