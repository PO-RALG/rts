# Generated by Django 5.0.2 on 2024-03-10 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_remove_book_phone_number_teacher_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='otp',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]