# Generated by Django 4.0 on 2022-09-29 11:42

from django.db import migrations, models
import django.utils.timezone
import employee.managers
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('lunch', '__first__'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=40, unique=True)),
                ('employee_number', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('cnic', models.CharField(max_length=100)),
                ('account_number', models.CharField(blank=True, max_length=100, null=True)),
                ('base_salary', models.IntegerField(blank=True, default=0)),
                ('status', models.CharField(choices=[('Permanent', 'Permanent'), ('Probation', 'Probation'), ('Intern', 'Intern')], default='Probation', max_length=15)),
                ('designation', models.CharField(blank=True, max_length=25)),
                ('phone', models.CharField(blank=True, max_length=15)),
                ('city', models.CharField(blank=True, max_length=50)),
                ('country', models.CharField(blank=True, max_length=50)),
                ('state', models.CharField(blank=True, max_length=50)),
                ('address', models.TextField(blank=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('lunch_menu', models.ManyToManyField(blank=True, related_name='for_employee', to='lunch.LunchMenu')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', employee.managers.UserManager()),
            ],
        ),
    ]