from django.db import models

class Journey(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    status = models.CharField(max_length=255)
    driver_id = models.CharField(max_length=255)
    patient_case_id = models.CharField(max_length=255)  # Corrected field name
    # route_id = models.CharField(max_length=255)
    route = models.ForeignKey('Route', on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'journey'


class Driver(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    license_number = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'driver'


class HealthcareFacility(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    name = models.CharField(max_length=255)
    location_lat = models.FloatField()
    location_lon = models.FloatField()

    class Meta:
        managed = False
        db_table = 'healthcare_facility'


class Route(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    start_type = models.CharField(max_length=255)
    end_type = models.CharField(max_length=255)
    # start_facility_id = models.CharField(max_length=255)
    # end_facility_id = models.CharField(max_length=255)
    start_village_id = models.CharField(max_length=255)
    start_port_id = models.CharField(max_length=255)
    end_port_id = models.CharField(max_length=255)
    start_facility = models.ForeignKey('HealthcareFacility', related_name='start_facility', on_delete=models.CASCADE)
    end_facility = models.ForeignKey('HealthcareFacility', related_name='end_facility', on_delete=models.CASCADE)
    class Meta:
        managed = False
        db_table = 'route'



# Create your models here.
# class Book(models.Model):
#     id = models.IntegerField(primary_key=True)
#     title = models.CharField(max_length=200, blank=True, null=True)
#     description = models.CharField(max_length=200, blank=True, null=True)
#     teacher = models.ForeignKey('Teacher', on_delete=models.DO_NOTHING, blank=True, null=True, related_name='books')
#     def __str__(self):
#         return self.title


class DriverJourney(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    driver_id = models.CharField(max_length=255, blank=True, null=True)  # Update max_length here
    journey_id = models.CharField(max_length=255, blank=True, null=True)  # Update max_length here
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"DriverJourney {self.id}"


# class Teacher(models.Model):
#     name = models.CharField(max_length=200, blank=True, null=True)
#     phone_number = models.CharField(max_length=200, blank=True, null=True)
#     otp = models.CharField(max_length=200, blank=True, null=True)
#
#     def __str__(self):
#         return f"Name: {self.name}, phoneNumber: {self.phone_number},otp: {self.otp}"



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

