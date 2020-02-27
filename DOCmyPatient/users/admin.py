from django.contrib import admin
from .models import DoctorProfile, PatientProfile, NurseProfile

admin.site.register(DoctorProfile)
admin.site.register(NurseProfile)
admin.site.register(PatientProfile)
