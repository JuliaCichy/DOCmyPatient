from django.contrib import admin
from .models import Profile, Doctor, Patient, Nurse

admin.site.register(Profile)
admin.site.register(Doctor)
admin.site.register(Nurse)
admin.site.register(Patient)
