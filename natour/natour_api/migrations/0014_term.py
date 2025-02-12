# Generated by Django 4.2.19 on 2025-02-11 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('natour_api', '0013_alter_customuser_date_of_birth_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Term',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('use_terms', models.TextField(blank=True, default='Termos de uso Natour')),
                ('politics', models.TextField(blank=True, default='Política de privacidade Natour')),
            ],
            options={
                'verbose_name': 'Term',
                'verbose_name_plural': 'Terms',
            },
        ),
    ]
