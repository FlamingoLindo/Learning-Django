# Generated by Django 5.1.5 on 2025-01-18 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('cpf', models.CharField(max_length=11)),
                ('password', models.CharField(max_length=100)),
                ('passwordConfirm', models.CharField(max_length=100, null=True)),
                ('role', models.CharField(max_length=100)),
                ('photo', models.ImageField(default='Images/doc.jpg', upload_to='Images/')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('date_of_birth', models.DateField()),
                ('phone_number', models.CharField(max_length=15)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
    ]
