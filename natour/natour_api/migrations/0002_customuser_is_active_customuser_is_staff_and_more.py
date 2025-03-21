# Generated by Django 5.1.5 on 2025-01-19 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('natour_api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='password',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='photo',
            field=models.ImageField(blank=True, default='Images/doc.jpg', null=True, upload_to='Images/'),
        ),
    ]
