from django.shortcuts import render
from .models import Comments

def home(request):
    context = {
        'comments': Comments.objects.all()
    }
    return render(request, 'docmypatient/patientZone.html', context)


notes = [
    {
        'id': 'Notes',
        'nurse_comment': '10/12/2019',
        'date_posted': 'Maura Murphy',
        'nurse_name': 'Today Mary was in good mood and had normal temperature of 37',


    },
    {
        'title': 'Notes',
        'date': '11/12/2019',
        'nurse': 'Maura Murphy',
        'note': 'Today Mary was feeling unwell, I have her Panadol',
        'wayne': 'fucking gorgeous'

    }
]