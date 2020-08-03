from django.test import TestCase
from django.contrib.auth.models import User
from users.models import Profile, Doctor, Patient
from django.test import Client


class PatientZoneTestCase(TestCase):

    def setUp(self):
        self.doctor = User.objects.create_user(username='testDoctor', password='12345')

        self.profile = Profile.objects.create(user=self.doctor, first_name="First Name", last_name="Last Name", dob="1917-08-26",
                                              sex="Male", is_doctor=True)

        self.doctor_profile = Doctor.objects.create(profile=self.profile, field="Brain", doc_reg_num=123)

    def test_get_patient_zone_not_logged_in(self):

        c = Client()
        response = c.get('/patientzone/')
        self.assertEqual(response.status_code, 302)
        self.assertNotContains(response, 'Patient List', status_code=302)

    def test_get_patient_zone_no_patients(self):

        c = Client()
        c.login(username='testDoctor', password='12345')
        response = c.get('/patientzone/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Patient List')
        self.assertNotContains(response, 'Bob')
        self.assertNotContains(response, 'George')

    def test_get_patient_zone(self):
        self.patient = User.objects.create_user(username='testPatient', password='12345')
        self.patientprofile = Profile.objects.create(user=self.patient, first_name="Bob", last_name="George",
                                                     dob="1917-08-26",
                                                     sex="Male", is_doctor=False, is_patient=True)
        Patient.objects.create(profile=self.patientprofile, doctor=self.doctor_profile, address="Address",
                               phone_number=123, ppsn=123)

        c = Client()
        c.login(username='testDoctor', password='12345')
        response = c.get('/patientzone/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Patient List')
        self.assertContains(response, 'Bob')
        self.assertContains(response, 'George')

    def test_get_patient_zone_multiple_patients(self):
        self.patient = User.objects.create_user(username='testPatient', password='12345')
        self.patientprofile = Profile.objects.create(user=self.patient, first_name="Bob", last_name="George",
                                                     dob="1917-08-26",
                                                     sex="Male", is_doctor=False, is_patient=True)
        Patient.objects.create(profile=self.patientprofile, doctor=self.doctor_profile, address="Address",
                               phone_number=123, ppsn=123)

        self.patient = User.objects.create_user(username='testPatient2', password='12345')
        self.patientprofile = Profile.objects.create(user=self.patient, first_name="John", last_name="Paul",
                                                     dob="1917-08-26",
                                                     sex="Male", is_doctor=False, is_patient=True)
        Patient.objects.create(profile=self.patientprofile, doctor=self.doctor_profile, address="Address",
                               phone_number=123, ppsn=12345)

        c = Client()
        c.login(username='testDoctor', password='12345')
        response = c.get('/patientzone/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Patient List')
        self.assertContains(response, 'Bob')
        self.assertContains(response, 'George')
        self.assertContains(response, 'Paul')
        self.assertContains(response, 'John')

    def test_get_patient_zone_multiple_patients_different_doctors(self):
        self.patient = User.objects.create_user(username='testPatient', password='12345')
        self.patientprofile = Profile.objects.create(user=self.patient, first_name="Bob", last_name="George",
                                                     dob="1917-08-26",
                                                     sex="Male", is_doctor=False, is_patient=True)
        Patient.objects.create(profile=self.patientprofile, doctor=self.doctor_profile, address="Address",
                               phone_number=123, ppsn=123)

        self.doctor = User.objects.create_user(username='testDoctor2', password='12345')

        self.profile = Profile.objects.create(user=self.doctor, first_name="First Name", last_name="Last Name",
                                              dob="1917-08-26",
                                              sex="Male", is_doctor=True)

        self.doctor_profile = Doctor.objects.create(profile=self.profile, field="Brain", doc_reg_num=123)

        self.patient = User.objects.create_user(username='testPatient2', password='12345')
        self.patientprofile = Profile.objects.create(user=self.patient, first_name="John", last_name="Paul",
                                                     dob="1917-08-26",
                                                     sex="Male", is_doctor=False, is_patient=True)
        Patient.objects.create(profile=self.patientprofile, doctor=self.doctor_profile, address="Address",
                               phone_number=123, ppsn=12345)

        c = Client()
        c.login(username='testDoctor', password='12345')
        response = c.get('/patientzone/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Patient List')
        self.assertContains(response, 'Bob')
        self.assertContains(response, 'George')
        self.assertNotContains(response, 'Paul')
        self.assertNotContains(response, 'John')
