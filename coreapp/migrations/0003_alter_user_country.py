# Generated by Django 4.1.1 on 2023-07-27 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coreapp', '0002_alter_user_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='country',
            field=models.CharField(default='Bangladesh', max_length=100),
        ),
    ]
