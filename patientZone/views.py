from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Comments
from .forms import CommentsForm
import datetime


def home(request):
    users = User.objects.all()
    users_list = []
    for user in users:
        try:
            if user.patient.doctor.id == request.user.doctor.id:
                users_list.append(user)
        except:
            continue
    context = {
        'users': users_list
    }
    return render(request, 'docmypatient/patientZone.html', context)


def patient(request, patient_id):
    try:
        patient = User.objects.get(id=patient_id)
        if patient.patient.doctor.id != request.user.doctor.id:
            raise Exception

        context = {"comments": Comments.objects.filter(patient_id=patient_id),
                   "patient": patient}

        return render(request, 'docmypatient/patientPage.html', context)

    except:
        return redirect('docmypatient')


def addComment(request, patient_id):
    # Check if the request is a POST method
    if request.method == 'POST':
        # Get the comment and user details from the request
        comment = request.POST.get('commentData')
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        now = datetime.datetime.now()

        # Post to the comments form
        comments_form = CommentsForm(data={'comment': comment,
                                           'date_posted': now,
                                           'staff_name': user,
                                           'patient_id': patient_id})
        # Check if its vaild
        if comments_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comments_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.comment = comment
            new_comment.staff_name = user
            new_comment.patient_id = patient_id
            # Save the comment to the database
            new_comment.save()

    return redirect('patientPage', patient_id=patient_id)


def deleteComment(request, patient_id, comment_id):
    if request.method == 'POST':
        comment = Comments.objects.get(id=comment_id)
        comment.delete()
        return redirect('patientPage', patient_id=patient_id)
    else:
        return redirect('docmypatient')


def openComment(request, patient_id, comment_id):
    if request.method == 'POST':
        comment = Comments.objects.get(id=comment_id)
        print(comment.date_posted)
        comment.opened = True
        print(comment.opened)
        comment.save()
        return redirect('patientPage', patient_id=patient_id)
    else:
        return redirect('docmypatient')
