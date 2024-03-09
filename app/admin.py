from django.contrib import admin
from .models import Book, Teacher, DriverAppSignal

# Register your models here.
admin.site.register(Book)
admin.site.register(Teacher)
admin.site.register(DriverAppSignal)

