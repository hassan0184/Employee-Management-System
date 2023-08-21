# Generated by Django 4.0 on 2023-01-13 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salary', '0002_alter_salary_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeductionAmount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('late_comers_amount', models.IntegerField()),
                ('absent_amount', models.IntegerField(null=True)),
            ],
            options={
                'verbose_name_plural': 'Deduction Amount Of Employees',
            },
        ),
    ]
