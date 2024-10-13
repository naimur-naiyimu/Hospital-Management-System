# Generated by Django 4.1.1 on 2023-07-27 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrations', '0004_remove_bed_patient_alter_ward_occupancy'),
        ('staff', '0002_alter_doctor_patients_staffleaveapplication_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='appointments',
            field=models.ManyToManyField(blank=True, null=True, related_name='doctors', to='administrations.appointment'),
        ),
    ]
