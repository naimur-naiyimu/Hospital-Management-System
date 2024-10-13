# Generated by Django 4.1.1 on 2023-08-18 09:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0007_alter_doctor_contact_number_and_more'),
        ('patient', '0007_alter_patient_contact_number'),
        ('coreapp', '0005_remove_user_dob_remove_user_image_alter_user_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='doctor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='staff.doctor'),
        ),
        migrations.AddField(
            model_name='user',
            name='patient',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='patient.patient'),
        ),
    ]
