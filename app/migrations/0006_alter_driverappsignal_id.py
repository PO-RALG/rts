# Generated by Django 5.0.2 on 2024-03-09 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_driverappsignal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driverappsignal',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]