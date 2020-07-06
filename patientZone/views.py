from django.shortcuts import render, redirect
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from users.models import Profile, Patient, Doctor
from .models import Comment
from .forms import CommentForm
import datetime
from django.contrib import messages


@login_required
def home(request):
    if request.user.profile.is_doctor:
        users = Profile.objects.filter(is_patient=True)
        users_list = []
        for user in users:
            if user.patient.doctor.id == request.user.profile.doctor.id:
                users_list.append(user)
        context = {
            'users': users_list
        }
        return render(request, 'docmypatient/patientZone.html', context)

    elif request.user.profile.is_nurse:
        users = Profile.objects.filter(is_patient=True)
        users_list = []
        for user in users:
            users_list.append(user)
        context = {
            'users': users_list
        }
        return render(request, 'docmypatient/patientZone.html', context)

    else:
        return redirect('logout')


def patient(request, patient_id):
    try:
        profile = Profile.objects.get(id=patient_id)
        if request.user.profile.is_doctor:
            if profile.patient.doctor.id != request.user.profile.doctor.id:
                raise Exception
        elif request.user.profile.is_nurse:
            pass
        else:
            raise Exception
        context = {"comments": Comment.objects.filter(patient_id=patient_id),
                   "patient": profile}

        return render(request, 'docmypatient/patientPage.html', context)

    except Exception as e:
        print(e)
        return redirect('docmypatient')


def edit_patient_page(request, patient_id):
    if request.method == 'POST':
        patient = Profile.objects.get(id=patient_id)
        doctors = Doctor.objects.all()
        doctors_list = []
        for doc in doctors:
            doctors_list.append(doc)
        date = patient.dob.strftime('%Y-%m-%d')
        return render(request, 'docmypatient/editPatient.html', {'patient': patient,
                                                                 'dob': date,
                                                                 'doctors': doctors_list,
                                                                 'patient_id': patient_id})
    else:
        return render(request, 'docmypatient/patientZone.html')


def edit_patient(request, patient_id):
    if request.method == 'POST':
        profile = Profile.objects.get(id=patient_id)
        patient_profile_id = profile.patient.id
        doctor = Doctor.objects.get(id=request.POST.get('doctor'))
        Profile.objects.filter(id=patient_id).update(first_name=request.POST.get('first_name'),
                                                     last_name=request.POST.get('last_name'),
                                                     dob=request.POST.get('dob'),
                                                     sex=request.POST.get('sex'))
        Patient.objects.filter(id=patient_profile_id).update(doctor=doctor,
                                                             address=request.POST.get('address'),
                                                             phone_number=request.POST.get('phone_number'),
                                                             ppsn=request.POST.get('ppsn'),
                                                             medical_card_num=request.POST.get('medical_card_num'),
                                                             emergency_contact=request.POST.get('emergency_contact'),
                                                             ec_phone_number=request.POST.get('ec_phone_number'),
                                                             ec_email_address=request.POST.get('ec_email_address'))

        return redirect('patientPage', patient_id)
    else:
        return render(request, 'docmypatient/patientZone.html')


def delete_patient(request, patient_id):
    if request.method == 'POST':
        Profile.objects.filter(id=patient_id).delete()

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
    if request.method == 'POST':
        if request.POST.get('first_name') and request.POST.get('last_name') \
                and request.POST.get('address') and request.POST.get('ppsn'):
            if check_user_exists(request.POST.get('ppsn')):
                profile = Profile.objects.create(first_name=request.POST.get('first_name'),
                                                 last_name=request.POST.get('last_name'),
                                                 dob=request.POST.get('dob'),
                                                 sex=request.POST.get('sex'),
                                                 is_patient=True)
                doctor = Doctor.objects.get(id=request.POST.get('doctor'))
                Patient.objects.create(profile=profile,
                                       doctor=doctor,
                                       address=request.POST.get('address'),
                                       phone_number=request.POST.get('phone_number'),
                                       ppsn=request.POST.get('ppsn'),
                                       medical_card_num=request.POST.get('medical_card_num'),
                                       emergency_contact=request.POST.get('emergency_contact'),
                                       ec_phone_number=request.POST.get('ec_phone_number'),
                                       ec_email_address=request.POST.get('ec_email_address'))
                return redirect('docmypatient')

            else:
                messages.error(request, "Error: A user with that PPSN already exists")
    doctors = Doctor.objects.all()
    doctors_list = []
    for doc in doctors:
        doctors_list.append(doc)

    return render(request, 'docmypatient/addPatient.html', {'doctors': doctors_list})


def check_user_exists(ppsn):
    if Patient.objects.filter(ppsn=ppsn).exists():
        return False
    else:
        return True
