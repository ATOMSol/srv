# Generated by Django 5.1.5 on 2025-01-23 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0007_rename_company_adress_appointment_company_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='status',
            field=models.CharField(choices=[('PENDING', 'Pending'), ('IN_PROGRESS', 'In Progress'), ('COMPLETED', 'Completed'), ('NEXT', 'Next')], default='PENDING', max_length=20),
        ),
    ]
