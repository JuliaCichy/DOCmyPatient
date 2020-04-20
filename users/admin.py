from django.contrib import admin
from .models import Doctor, Patient, Nurse

admin.site.register(Doctor)
admin.site.register(Nurse)
admin.site.register(Patient)
