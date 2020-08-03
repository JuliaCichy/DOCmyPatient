from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from patientZone.models import Comment
from users.models import Profile, Doctor, Patient
from django.test import Client
from django.utils import timezone


class PatientPageTestCase(TestCase):

    def setUp(self):
        self.doctor = User.objects.create_user(username='testDoctor', password='12345')

        self.profile = Profile.objects.create(user=self.doctor, first_name="First Name", last_name="Last Name",
                                              dob="1917-08-26", sex="Male", is_doctor=True)

        self.doctor_profile = Doctor.objects.create(profile=self.profile, field="Brain", doc_reg_num=123)

        self.patient = User.objects.create_user(username='testPatient', password='12345')
        self.patientprofile = Profile.objects.create(user=self.patient, first_name="Bob", last_name="George",
                                                     dob="1917-08-26",
                                                     sex="Male", is_doctor=False, is_patient=True)
        Patient.objects.create(profile=self.patientprofile, doctor=self.doctor_profile, address="Address",
                               phone_number=123, ppsn=123)

    def test_get_patient_page_not_logged_in(self):
        c = Client()
        response = c.get(reverse('patientPage', kwargs={'patient_id': self.patientprofile.id}))
        self.assertEqual(response.status_code, 302)

    def test_get_patient_page_logged_in(self):
        c = Client()
        c.login(username='testDoctor', password='12345')
        response = c.get(reverse('patientPage', kwargs={'patient_id': self.patientprofile.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Patient details')
        self.assertContains(response, 'Bob')
        self.assertContains(response, 'George')
        self.assertNotContains(response, 'Michael')

    def test_get_patient_page_comments(self):
        Comment.objects.create(comment="Test Comment", date_posted=timezone.now(), show_patient=False,
                               staff_name=self.doctor, staff_id=123, patient_id=self.patientprofile.id, patient="Bob George", opened=False)

        Comment.objects.create(comment="Test Comment 2", date_posted=timezone.now(), show_patient=False,
                               staff_name=self.doctor, staff_id=123, patient_id=self.patientprofile.id, patient="Bob George", opened=False)

        Comment.objects.create(comment="Test Comment 3", date_posted=timezone.now(), show_patient=False,
                               staff_name=self.doctor, staff_id=123, patient_id=12, patient="Jimmy", opened=False)

        c = Client()
        c.login(username='testDoctor', password='12345')
        response = c.get(reverse('patientPage', kwargs={'patient_id': self.patientprofile.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Patient details')
        self.assertContains(response, 'Bob')
        self.assertContains(response, 'George')
        self.assertContains(response, 'Male')
        self.assertContains(response, 'Address')
        self.assertContains(response, 'Test Comment')
        self.assertContains(response, 'Test Comment 2')
        self.assertNotContains(response, 'Test Comment 3')

    def test_add_comment_patient_page(self):
        c = Client()
        c.login(username='testDoctor', password='12345')
        response = c.post(reverse('addPatientComment', kwargs={'patient_id': self.patientprofile.id}),
                          {'comment': "Test New Comment"})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/patientzone/{}'.format(self.patientprofile.id), status_code=302)

    def test_delete_comment_patient_page(self):
        Comment.objects.create(comment="Test Comment", date_posted=timezone.now(), show_patient=False,
                               staff_name=self.doctor, staff_id=123, patient_id=self.patientprofile.id,
                               patient="Bob George", opened=False)

        c = Client()
        c.login(username='testDoctor', password='12345')
        response = c.post(reverse('deletePatientComment', kwargs={'patient_id': self.patientprofile.id, 'comment_id': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/patientzone/{}'.format(self.patientprofile.id), status_code=302)

    def test_open_comment_patient_page(self):
        Comment.objects.create(comment="Test Comment", date_posted=timezone.now(), show_patient=False,
                               staff_name=self.doctor, staff_id=123, patient_id=self.patientprofile.id,
                               patient="Bob George", opened=False)

        c = Client()
        c.login(username='testDoctor', password='12345')
        response = c.post(reverse('openPatientComment', kwargs={'patient_id': self.patientprofile.id, 'comment_id': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/patientzone/{}'.format(self.patientprofile.id), status_code=302)

    def test_get_edit_patient_page(self):
        c = Client()
        c.login(username='testDoctor', password='12345')
        response = c.post(reverse('editPatientPage', kwargs={'patient_id': self.patientprofile.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Edit patient profile')
        self.assertContains(response, 'Bob')
        self.assertContains(response, 'George')

    def test_get_edit_patient_page_not_logged_in(self):
        c = Client()
        response = c.post(reverse('editPatientPage', kwargs={'patient_id': self.patientprofile.id}))
        self.assertEqual(response.status_code, 302)

    def test_edit_patient(self):
        c = Client()
        c.login(username='testDoctor', password='12345')
        response = c.post(reverse('editPatient', kwargs={'patient_id': self.patientprofile.id}),
                          {'first_name': "Bobby",
                           'last_name': "Georgy",
                           'dob': "1917-08-26",
                           'sex': "Male",
                           'doctor': self.doctor_profile.id,
                           'address': "Address",
                           'phone_number': 1234,
                           'ppsn': 123242,
                           'medical_card_num': 123})

        self.assertEqual(response.status_code, 302)
