# Generated by Django 4.0 on 2023-01-12 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_annocument'),
    ]

    operations = [
        migrations.AlterField(
            model_name='annocument',
            name='date_time',
            field=models.DateField(blank=True, null=True),
        ),
    ]