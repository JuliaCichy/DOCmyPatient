from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Comment
from .forms import CommentForm
import datetime


@login_required
def home(request):
    if request.user.profile.is_doctor:
        users = User.objects.all()
        users_list = []
        for user in users:
            if user.profile.is_patient and user.profile.patient.doctor.id == request.user.profile.doctor.id:
                users_list.append(user)
        context = {
            'users': users_list
        }
        return render(request, 'docmypatient/patientZone.html', context)

    elif request.user.profile.is_nurse:
        users = User.objects.all()
        users_list = []
        for user in users:
            if user.profile.is_patient:
                users_list.append(user)
        context = {
            'users': users_list
        }
        return render(request, 'docmypatient/patientZone.html', context)

    else:
        return redirect('logout')


def patient(request, patient_id):
    try:
        patient = User.objects.get(id=patient_id)
        if request.user.profile.is_doctor:
            if patient.profile.patient.doctor.id != request.user.profile.doctor.id:
                raise Exception
        elif request.user.profile.is_nurse:
            pass
        else:
            raise Exception

        context = {"comments": Comment.objects.filter(patient_id=patient_id),
                   "patient": patient}

        return render(request, 'docmypatient/patientPage.html', context)

    except:
        return redirect('docmypatient')


def add_comment(request, patient_id):
    # Check if the request is a POST method
    if request.method == 'POST':
        # Get the comment and user details from the request
        comment = request.POST.get('commentData')
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        now = datetime.datetime.now()

        # Post to the comments form
        comments_form = CommentForm(data={'comment': comment,
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


def delete_comment(request, patient_id, comment_id):
    if request.method == 'POST':
        comment = Comment.objects.get(id=comment_id)
        comment.delete()
        return redirect('patientPage', patient_id=patient_id)
    else:
        return redirect('docmypatient')


def open_comment(request, patient_id, comment_id):
    if request.method == 'POST':
        comment = Comment.objects.get(id=comment_id)
        print(comment.date_posted)
        comment.opened = True
        print(comment.opened)
        comment.save()
        return redirect('patientPage', patient_id=patient_id)
    else:
        return redirect('docmypatient')


def add_patient(request):
    print("HELLO THERE")
    if request.method == 'POST':
        return render(request, 'docmypatient/addPatient.html')
    else:
        return render(request, 'docmypatient/addPatient.html')

