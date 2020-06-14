from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='docmypatient'),
    path('<patient_id>', views.patient, name='patientPage'),
    path('<patient_id>/addComment', views.addComment, name='addPatientComment'),
    path('<patient_id>/deleteComment/<comment_id>/', views.deleteComment, name='deletePatientComment'),
    path('<patient_id>/openComment/<comment_id>/', views.openComment, name='openPatientComment')
]
