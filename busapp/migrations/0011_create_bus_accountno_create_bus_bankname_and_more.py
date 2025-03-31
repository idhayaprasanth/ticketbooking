# Generated by Django 4.2.2 on 2023-07-16 07:20

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('busapp', '0010_remove_create_bus_busroute_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='create_bus',
            name='accountno',
            field=models.IntegerField(default='0', unique=True),
        ),
        migrations.AddField(
            model_name='create_bus',
            name='bankname',
            field=models.CharField(default='BankName', max_length=500),
        ),
        migrations.AddField(
            model_name='create_bus',
            name='ifsc',
            field=models.CharField(default='A1', max_length=100, validators=[django.core.validators.RegexValidator(message='Field must contain at least one letter and one number.', regex='^(?=.*[a-zA-Z])(?=.*\\d)[a-zA-Z\\d]+$'), django.core.validators.MinLengthValidator(8)]),
        ),
    ]
