# Generated by Django 4.0 on 2023-01-12 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_alter_annocument_date_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='annocument',
            name='date_time',
        ),
        migrations.AddField(
            model_name='annocument',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
