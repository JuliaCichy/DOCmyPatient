from django.shortcuts import render
from .models import Comments


def home(request):
    context = {
        'comments': Comments.objects.all()
    }
    return render(request, 'docmypatient/patientZone.html', context)
