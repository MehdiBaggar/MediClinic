from django.contrib import admin
from .models import Doctor

class DoctorAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'gender', 'speciality', 'phone', 'bio')





admin.site.register(Doctor, DoctorAdmin)