# Generated by Django 5.0.2 on 2024-03-25 15:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_journey_driverjourney'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Book',
        ),
        migrations.DeleteModel(
            name='Teacher',
        ),
    ]
