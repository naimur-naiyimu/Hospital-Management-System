# Generated by Django 4.1.1 on 2023-08-29 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0010_alter_patient_emergency_gender_alter_patient_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='emergency_gender',
            field=models.SmallIntegerField(choices=[(0, 'Male'), (1, 'Female'), (2, 'Other')], default=0),
        ),
    ]
