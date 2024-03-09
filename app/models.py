from django.db import models

# Create your models here.
class Book(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    teacher = models.ForeignKey('Teacher', on_delete=models.DO_NOTHING, blank=True, null=True, related_name='books')

    def __str__(self):
        return self.title


class Teacher(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name


class DriverAppSignal(models.Model):
    id = models.AutoField(primary_key=True)
    signal_data = models.CharField(max_length=200, blank=True, null=True)
    device_imei = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.signal_data
