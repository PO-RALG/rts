# Generated by Django 5.0.2 on 2024-03-09 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_driverappsignal_device_imei_alter_driverappsignal_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driverappsignal',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
