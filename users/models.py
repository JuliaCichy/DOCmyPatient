from django.db import models
from django.contrib.auth.models import User

SEX = (
    ('F', 'Female'),
    ('M', 'Male'),
    ('O', 'Other'),
)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    dob = models.DateField()
    sex = models.CharField(max_length=1, choices=SEX)
    is_nurse = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Doctor(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    field = models.CharField(max_length=200)
    doc_reg_num = models.CharField(max_length=25)

    def __str__(self):
        return self.profile.user.username


class Nurse(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    ward = models.CharField(max_length=25)

    def __str__(self):
        return self.profile.user.username


class Patient(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=100)
    phone_number = models.IntegerField()
    ppsn = models.CharField(max_length=15)
    medical_card_num = models.CharField(max_length=15, null=True)
    emergency_contact = models.CharField(max_length=15, null=True)
    ec_phone_number = models.IntegerField()

    def __str__(self):
        return self.profile.user.username

