from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from PIL import Image
from resizeimage import resizeimage
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

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
class Person(models.Model):
    full_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.SmallIntegerField(choices=GENDER_CHOICES,default=1)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES, default='A+')
    address = models.CharField(max_length=150)
    contact_number = models.CharField(unique=True, max_length=20)
    salary = models.IntegerField()
    photo = models.ImageField(upload_to='doctor_photos/', null=True, blank=True)

    class Meta:
        abstract = True 

class Doctor(Person):
    specialization = models.CharField(max_length=100)
    certificate = models.CharField(max_length=100)
    fees = models.IntegerField(null=True, blank=True)
    patients = models.ManyToManyField('patient.Patient', blank= True, null=True)
    appointments = models.ManyToManyField('administrations.Appointment', related_name='doctors',blank= True, null=True)

    def __str__(self):
        return f"{self.full_name} - {self.specialization}"

class Staff(Person):
    role = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.full_name} - {self.role}"
    
@receiver(pre_save, sender=Doctor)
@receiver(pre_save, sender=Staff)
def resize_photo_on_save(sender, instance, **kwargs):
    if instance.photo:
        try:
            img = Image.open(instance.photo)
        except:
            print("not image")
            return
        
        max_size = (400, 300)  # Set the desired size here (width, height)

        if img.height > max_size[1] or img.width > max_size[0]:
            img = resizeimage.resize_cover(img, max_size, validate=False)
            img_io = BytesIO()
            img.save(img_io, format=img.format, quality=80)
            instance.photo = InMemoryUploadedFile(
                img_io,
                None,
                f'{instance.photo.name.split(".")[0]}.{img.format.lower()}',
                f'image/{img.format.lower()}',
                img_io.getbuffer().nbytes,
                None
            )


class DoctorAttendance(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    is_present = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.doctor} - {self.date} - Present: {self.is_present}"

class StaffAttendance(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    date = models.DateField()
    is_present = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.staff} - {self.date} - Present: {self.is_present}"

class DoctorLeaveApplication(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    leave_start_date = models.DateField()
    leave_end_date = models.DateField()
    reason = models.TextField()
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.doctor} - {self.leave_start_date} to {self.leave_end_date} - Approved: {self.is_approved}"

class StaffLeaveApplication(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    leave_start_date = models.DateField()
    leave_end_date = models.DateField()
    reason = models.TextField()
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.staff} - {self.leave_start_date} to {self.leave_end_date} - Approved: {self.is_approved}"

