# Generated by Django 4.1.1 on 2023-08-15 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0006_patient_allocated_bed_patient_ward'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='contact_number',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
