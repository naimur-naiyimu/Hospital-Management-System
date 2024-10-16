# Generated by Django 4.1.1 on 2023-08-07 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrations', '0010_bed_ward'),
    ]

    operations = [
        migrations.AddField(
            model_name='prescription',
            name='test',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='prescription',
            name='dosage',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='prescription',
            name='instructions',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='prescription',
            name='medication',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='prescription',
            name='next_appointment_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
