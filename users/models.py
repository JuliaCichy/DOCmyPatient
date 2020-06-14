from django.db import models
from django.contrib.auth.models import User

SEX = (
    ('F', 'Female'),
    ('M', 'Male'),
    ('O', 'Other'),
)


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    field = models.CharField(max_length=200)
    doc_reg_num = models.CharField(max_length=25)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    dob = models.DateField()
    sex = models.CharField(max_length=1, choices=SEX)

    def __str__(self):
        return self.user.username


class Nurse(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ward = models.CharField(max_length=25)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    dob = models.DateField()
    sex = models.CharField(max_length=1, choices=SEX)

    def __str__(self):
        return self.user.username


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=100)
    phone_number = models.IntegerField()
    ppsn = models.CharField(max_length=15)
    medical_card_num = models.CharField(max_length=15, null=True)
    emergency_contact = models.CharField(max_length=15, null=True)
    ec_phone_number = models.IntegerField(null=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    dob = models.DateField()
    sex = models.CharField(max_length=1, choices=SEX)

    def __str__(self):
        return self.user.username
