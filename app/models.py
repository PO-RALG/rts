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
    phone_number = models.CharField(max_length=200, blank=True, null=True)
    otp = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"Name: {self.name}, phoneNumber: {self.phone_number},otp: {self.otp}"



class DriverAppSignal(models.Model):
    id = models.AutoField(primary_key=True)
    device_id = models.CharField(max_length=200, blank=True, null=True)
    driver_id = models.CharField(max_length=200, blank=True, null=True)
    device_imei = models.CharField(max_length=200, blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"latitude: {self.latitude}, longitude: {self.longitude}"

