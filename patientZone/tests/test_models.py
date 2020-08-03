from django.test import TestCase
from django.contrib.auth.models import User
from patientZone.models import Comment, UploadedFile
from django.utils import timezone


class CommentTestCase(TestCase):
    def setUp(self):
        self.doctor = User.objects.create_user(username='testDoctor', password='12345')
        self.client.login(username='testDoctor', password='12345')

    def tearDown(self):
        # Clean up run after every test method.
        Comment.objects.all().delete()
 
    def test_get_no_comments(self):
        comment = Comment.objects.filter(patient_id=1)
        self.assertEqual(len(comment), 0)

    def test_get_comments_same_patient(self):
        Comment.objects.create(comment="Test Comment", date_posted=timezone.now(), show_patient=False,
                               staff_name=self.doctor, staff_id=123, patient_id=1, patient="TestPatient", opened=False)

        Comment.objects.create(comment="Test Comment 2", date_posted=timezone.now(), show_patient=False,
                               staff_name=self.doctor, staff_id=123, patient_id=1, patient="TestPatient", opened=False)

        comment = Comment.objects.filter(patient_id=1)
        self.assertEqual(comment[0].comment, 'Test Comment')
        self.assertEqual(comment[0].show_patient, False)
        self.assertEqual(comment[1].comment, 'Test Comment 2')
        self.assertEqual(comment[1].show_patient, False)
        self.assertEqual(len(comment), 2)

    def test_get_comments_different_patient(self):
        Comment.objects.create(comment="Test Comment", date_posted=timezone.now(), show_patient=False,
                               staff_name=self.doctor, staff_id=123, patient_id=1, patient="TestPatient", opened=False)

        Comment.objects.create(comment="Test Comment 2", date_posted=timezone.now(), show_patient=False,
                               staff_name=self.doctor, staff_id=123, patient_id=2, patient="TestPatient", opened=False)

        comment = Comment.objects.filter(patient_id=1)
        self.assertEqual(comment[0].comment, 'Test Comment')
        self.assertEqual(comment[0].show_patient, False)
        self.assertEqual(len(comment), 1)


class UploadedFileTestCase(TestCase):
    def setUp(self):
        self.doctor = User.objects.create_user(username='testDoctor', password='12345')
        self.client.login(username='testDoctor', password='12345')

    def tearDown(self):
        # Clean up run after every test method.
        UploadedFile.objects.all().delete()

    def test_no_uploads(self):
        uploaded_files = UploadedFile.objects.all()
        self.assertEqual(len(uploaded_files), 0)

    def test_uploading_file(self):
        UploadedFile.objects.create(file_title="Test_file.png", date_posted=timezone.now(),
                                    staff_name=self.doctor, staff_id=123, patient_id=1, patient="test patient",
                                    uploaded_file="Test_file.png")

        uploaded_files = UploadedFile.objects.filter(patient_id=1)
        self.assertEqual(uploaded_files[0].file_title, 'Test_file.png')
        self.assertEqual(uploaded_files[0].patient, 'test patient')
        self.assertEqual(len(uploaded_files), 1)

    def test_get_multiple_file(self):
        UploadedFile.objects.create(file_title="Test_file.png", date_posted=timezone.now(),
                                    staff_name=self.doctor, staff_id=123, patient_id=1, patient="test patient",
                                    uploaded_file="Test_file.png")

        UploadedFile.objects.create(file_title="Test_file_2.png", date_posted=timezone.now(),
                                    staff_name=self.doctor, staff_id=123, patient_id=1, patient="test patient",
                                    uploaded_file="Test_file.png")

        uploaded_files = UploadedFile.objects.filter(patient_id=1)
        self.assertEqual(uploaded_files[0].file_title, 'Test_file.png')
        self.assertEqual(uploaded_files[0].patient, 'test patient')
        self.assertEqual(uploaded_files[1].file_title, 'Test_file_2.png')
        self.assertEqual(uploaded_files[1].patient, 'test patient')
        self.assertEqual(len(uploaded_files), 2)

    def test_get_multiple_file_dif_patient(self):
        UploadedFile.objects.create(file_title="Test_file.png", date_posted=timezone.now(),
                                    staff_name=self.doctor, staff_id=123, patient_id=1, patient="test patient",
                                    uploaded_file="Test_file.png")

        UploadedFile.objects.create(file_title="Test_file_2.png", date_posted=timezone.now(),
                                    staff_name=self.doctor, staff_id=123, patient_id=2, patient="test patient",
                                    uploaded_file="Test_file.png")

        uploaded_files = UploadedFile.objects.filter(patient_id=1)
        self.assertEqual(uploaded_files[0].file_title, 'Test_file.png')
        self.assertEqual(uploaded_files[0].patient, 'test patient')
        self.assertEqual(len(uploaded_files), 1)
