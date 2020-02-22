from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='docmypatient'),
    path('addComment', views.addComment, name='addPatientComment'),
]