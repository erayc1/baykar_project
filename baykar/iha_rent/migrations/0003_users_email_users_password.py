# Generated by Django 5.0.6 on 2024-05-18 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iha_rent', '0002_ihadetails_rentrecords'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='email',
            field=models.CharField(default='default@example.com', max_length=100),
        ),
        migrations.AddField(
            model_name='users',
            name='password',
            field=models.CharField(default='123456', max_length=100),
        ),
    ]