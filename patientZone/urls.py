from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='docmypatient'),
    path('<user_id>', views.patient, name='patientPage'),
    path('addComment', views.addComment, name='addPatientComment'),
]