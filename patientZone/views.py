from django.shortcuts import render, redirect
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from users.models import Profile, Patient, Doctor
from .models import Comment
from .forms import CommentForm
from .utils import get_profile_reference, check_user_exists
import datetime
from django.contrib import messages
from django.core.mail import send_mail


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
        return redirect('profile')


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
        context = {"comments": Comment.objects.filter(patient_id=patient_id).order_by('-date_posted'),
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
        patient_name = Profile.objects.get(id=patient_id)
        user = User.objects.get(id=user_id)
        now = datetime.datetime.now()
        show_patient = False
        if request.POST.get('forPatient') == "True":
            show_patient = True

        # Post to the comments form
        comments_form = CommentForm(data={'comment': comment,
                                           'date_posted': now,
                                           'staff_name': user,
                                           'pateint': patient_name,
                                           'staff_id': user.profile.id,
                                           'patient_id': patient_id,
                                           'show_patient': show_patient})
        # Check if its vaild
        if comments_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comments_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.comment = comment
            new_comment.staff_name = user
            new_comment.staff_id = user.profile.id
            new_comment.patient_id = patient_id
            new_comment.patient = patient_name
            new_comment.show_patient = show_patient
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
                                                 is_patient=True,
                                                 profile_reference=get_profile_reference())

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

                if request.POST.get('ec_email_address'):
                    send_mail(
                        'Doc Your Patient',
                        'Dear {} you have been logged in as an Emergency Contact for {}, if you would like to check'
                        ' their progress please follow the following link! \n'
                        'http://127.0.0.1:8000/register/{}/?reference={}'.format(profile.patient.emergency_contact, profile, profile.id, profile.profile_reference),
                        'x16369733@student.ncirl.ie',
                        [request.POST.get('ec_email_address')],
                        fail_silently=False,
                    )
                return redirect('docmypatient')

            else:
                messages.error(request, "Error: A user with that PPSN already exists")
    doctors = Doctor.objects.all()
    doctors_list = []
    for doc in doctors:
        doctors_list.append(doc)

    return render(request, 'docmypatient/addPatient.html', {'doctors': doctors_list})
