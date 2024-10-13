# Generated by Django 4.1.1 on 2023-08-08 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrations', '0012_remove_labtest_patient'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medicalreport',
            name='doctor',
        ),
        migrations.RemoveField(
            model_name='medicalreport',
            name='is_admited',
        ),
        migrations.RemoveField(
            model_name='medicalreport',
            name='is_outdoor',
        ),
        migrations.RemoveField(
            model_name='medicalreport',
            name='is_surgery',
        ),
        migrations.RemoveField(
            model_name='medicalreport',
            name='is_transfer',
        ),
        migrations.RemoveField(
            model_name='medicalreport',
            name='lab_tests',
        ),
        migrations.RemoveField(
            model_name='medicalreport',
            name='report_date',
        ),
        migrations.AddField(
            model_name='medicalreport',
            name='delivery_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='medicalreport',
            name='report_file',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='medicalreport',
            name='results',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='medicalreport',
            name='test_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='medicalreport',
            name='test_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.DeleteModel(
            name='LabTest',
        ),
    ]
