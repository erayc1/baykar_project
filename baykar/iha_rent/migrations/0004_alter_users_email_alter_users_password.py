# Generated by Django 5.0.6 on 2024-05-18 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iha_rent', '0003_users_email_users_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='email',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='password',
            field=models.CharField(max_length=100),
        ),
    ]
