# Generated by Django 4.2.2 on 2023-07-15 16:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('busapp', '0007_delete_comparisonmodel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='create_bus',
            name='image',
        ),
    ]
