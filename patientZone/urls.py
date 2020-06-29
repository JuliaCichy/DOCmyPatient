from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='docmypatient'),
    path('<patient_id>', views.patient, name='patientPage'),
    path('<patient_id>/addComment', views.add_comment, name='addPatientComment'),
    path('<patient_id>/deleteComment/<comment_id>/', views.delete_comment, name='deletePatientComment'),
    path('<patient_id>/openComment/<comment_id>/', views.open_comment, name='openPatientComment'),
    path('add-patient/', views.add_patient, name='addPatient')
]
