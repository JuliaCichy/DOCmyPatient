from django.shortcuts import render, redirect
from .models import Comments


def home(request):
    context = {
        'comments': Comments.objects.all()
    }
    return render(request, 'docmypatient/patientZone.html', context)


def addComment(request):
    if request == 'POST':

        nurse_comment = request.POST.get('commentData')
        current_user = request.user
        comment = Comments(nurse_comment=nurse_comment, nurse_name=current_user)

        if form.is_valid():
            comment.save()
            messages.success(request,"Comment added!")
            return redirect('docmypatient')

    else:
        return redirect('docmypatient')

