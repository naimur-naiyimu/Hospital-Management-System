# Generated by Django 4.1.1 on 2023-07-27 09:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('staff', '0001_initial'),
        ('administrations', '0001_initial'),
        ('patient', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='prescription',
            name='doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doctor_prescriptions', to='staff.doctor'),
        ),
        migrations.AddField(
            model_name='prescription',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prescriptions', to='patient.patient'),
        ),
        migrations.AddField(
            model_name='medicalreport',
            name='doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doctor_medical_reports', to='staff.doctor'),
        ),
        migrations.AddField(
            model_name='medicalreport',
            name='lab_test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administrations.labtest'),
        ),
        migrations.AddField(
            model_name='medicalreport',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medical_reports', to='patient.patient'),
        ),
        migrations.AddField(
            model_name='labtest',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patient.patient'),
        ),
        migrations.AddField(
            model_name='billing',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patient.patient'),
        ),
        migrations.AddField(
            model_name='bed',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='beds', to='patient.patient'),
        ),
        migrations.AddField(
            model_name='bed',
            name='ward',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administrations.ward'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doctor_appointments', to='staff.doctor'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to='patient.patient'),
        ),
    ]
