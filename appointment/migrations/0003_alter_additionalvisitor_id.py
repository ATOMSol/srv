# Generated by Django 5.1.5 on 2025-02-27 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0002_alter_additionalvisitor_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='additionalvisitor',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
