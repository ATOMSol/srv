# Generated by Django 4.0.5 on 2025-02-04 21:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('appointment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='assigned_to',
            field=models.ForeignKey(blank=True, limit_choices_to={'roles__name': 'gm'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_appointments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='appointment',
            name='created_by',
            field=models.ForeignKey(blank=True, limit_choices_to={'roles__name': 'pa'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_appointments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='appointment',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_appointments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='additionalvisitor',
            name='participants',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='additional_visitor', to='appointment.appointment'),
        ),
    ]
