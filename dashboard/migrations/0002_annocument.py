# Generated by Django 4.0 on 2023-01-12 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Annocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('annoucment', models.TextField(blank=True, null=True)),
                ('date_time', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]
