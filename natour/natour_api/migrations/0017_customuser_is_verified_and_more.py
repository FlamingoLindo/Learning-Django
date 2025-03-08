# Generated by Django 4.2.19 on 2025-03-08 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('natour_api', '0016_remove_customuser_is_staff_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customuser',
            name='verification_expires',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
