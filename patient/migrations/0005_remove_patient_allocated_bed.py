# Generated by Django 4.1.1 on 2023-08-07 05:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0004_remove_patient_emergency_contact_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='allocated_bed',
        ),
    ]
