# Generated by Django 4.2.2 on 2023-07-16 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('busapp', '0009_delete_tickets_create_bus_ticket1_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='create_bus',
            name='busroute',
        ),
        migrations.RemoveField(
            model_name='create_bus',
            name='busstops',
        ),
        migrations.RemoveField(
            model_name='create_bus',
            name='bustime',
        ),
        migrations.RemoveField(
            model_name='create_bus',
            name='disno',
        ),
        migrations.RemoveField(
            model_name='create_bus',
            name='routeno',
        ),
        migrations.AddField(
            model_name='create_bus',
            name='busname',
            field=models.CharField(default='name', max_length=500),
        ),
        migrations.AddField(
            model_name='create_bus',
            name='contact',
            field=models.IntegerField(default='0'),
        ),
    ]