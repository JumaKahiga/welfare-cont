# Generated by Django 3.0.2 on 2020-01-10 16:54

import cloudinary.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('avatar', cloudinary.models.CloudinaryField(default='image/upload/v1551960935/books.png', max_length=255, verbose_name='image')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('email', models.CharField(max_length=50, unique=True)),
                ('phone_number', models.PositiveIntegerField(unique=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Dependant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('avatar', cloudinary.models.CloudinaryField(default='image/upload/v1551960935/books.png', max_length=255, verbose_name='image')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('relationship', models.CharField(choices=[('Spouse', 'Spouse'), ('Child', 'Child')], max_length=15)),
                ('principal_member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_dependants', to='members.Member')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
