# Generated by Django 5.1.5 on 2025-02-27 19:19

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('visitor_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=15)),
                ('date', models.DateField()),
                ('description', models.TextField(blank=True)),
                ('status', models.CharField(choices=[('pending', 'pending'), ('in_progress', 'In Progress'), ('completed', 'Completed'), ('next', 'Next'), ('call', 'Call')], default='pending', max_length=20)),
                ('company_name', models.CharField(default='NA', max_length=100)),
                ('company_address', models.CharField(default='NA', max_length=100)),
                ('purpose_of_visit', models.CharField(default='Na', max_length=100)),
                ('visitor_img', models.ImageField(blank=True, upload_to='visitor_img/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('assigned_to', models.ForeignKey(blank=True, limit_choices_to={'roles__name': 'gm'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_appointments', to=settings.AUTH_USER_MODEL)),
                ('created_by', models.ForeignKey(blank=True, limit_choices_to={'roles__name': 'pa'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_appointments', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_appointments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AdditionalVisitor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('img', models.ImageField(blank=True, upload_to='additional_visitor_image/')),
                ('participants', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='additional_visitors', to='appointment.appointment')),
            ],
        ),
    ]
