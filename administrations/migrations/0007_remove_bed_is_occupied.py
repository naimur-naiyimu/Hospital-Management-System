# Generated by Django 4.1.1 on 2023-08-04 10:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('administrations', '0006_remove_ward_department_ward_contact_number_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bed',
            name='is_occupied',
        ),
    ]
