# Generated by Django 4.0 on 2023-01-11 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0014_employee_checkin_time_alter_employee_time_slot'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkin',
            name='checkin_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='checkin',
            name='checkin_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
