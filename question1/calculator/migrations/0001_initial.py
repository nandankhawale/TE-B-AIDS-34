# Generated by Django 5.2.1 on 2025-06-04 05:53

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AuthToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access_token', models.TextField()),
                ('token_type', models.CharField(default='Bearer', max_length=50)),
                ('expires_in', models.BigIntegerField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='NumberEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('p', 'Prime'), ('f', 'Fibonacci'), ('e', 'Even'), ('r', 'Random')], max_length=1)),
                ('number', models.IntegerField()),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'ordering': ['-timestamp'],
                'unique_together': {('category', 'number')},
            },
        ),
    ]
