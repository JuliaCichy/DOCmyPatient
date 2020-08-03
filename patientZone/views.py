from django.shortcuts import render, redirect
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from users.models import Profile, Patient, Doctor
from .models import Comment, UploadedFile
from .forms import CommentForm
from .utils import get_profile_reference, check_user_exists
import datetime
from django.contrib import messages
from django.core.mail import send_mail
import os
from django.conf import settings
from django.http import HttpResponse, Http404


# @login_required ensures the user accessing the page is logged in (Redirects to login page if not)
@login_required
def home(request):
    """View for home page (PatientZone)"""

    # Checks if the current user is a Doctor or a Nurse, else redirects the user to the profile page
    # This stops anyone from getting to this page
    if request.user.profile.is_doctor:
        # Gets all users that are patients and checks if the
        # doctor id attached to them is the same as the current doctors ID
        users = Profile.objects.filter(is_patient=True)
        users_list = []
        for user in users:
            if user.patient.doctor.id == request.user.profile.doctor.id:
                users_list.append(user)
        context = {
            'users': users_list
        }
        # Returns the template with all patients
        return render(request, 'docmypatient/patientZone.html', context)

    elif request.user.profile.is_nurse:
        # A nurse has access to all patients, so no need to filter by doctor ID
        users = Profile.objects.filter(is_patient=True)
        users_list = []
        for user in users:
            users_list.append(user)
        context = {
            'users': users_list
        }
        return render(request, 'docmypatient/patientZone.html', context)

    else:
        # Returns profile page if user is not a doctor or nurse
        return redirect('profile')


@login_required
def patient(request, patient_id):
    """This is the view for the patientPage that the nurse/doctor see
        The patient ID is passed in as a parameter in the URL "<patient_id>" """
    try:
        # Gets the patient Profile from the URL
        profile = Profile.objects.get(id=patient_id)
        # Makes a check to see if the current user is a doctor or nurse (permissions)
        if request.user.profile.is_doctor:
            if profile.patient.doctor.id != request.user.profile.doctor.id:
                raise Exception
        elif request.user.profile.is_nurse:
            pass
        else:
            # If not a nurse or doctor raise exception
            raise Exception

        # Gets all comments and files uploaded attached to that patient's profile
        # Creates a Json object to return
        context = {"comments": Comment.objects.filter(patient_id=patient_id).order_by('-date_posted'),
                   "files": UploadedFile.objects.filter(patient_id=patient_id).order_by('-date_posted'),
                   "patient": profile}

        # Returns the template with the Json object
        return render(request, 'docmypatient/patientPage.html', context)

    except Exception as e:
        # If an exception is found, redirect the user back to the PatientZOne page
        print(e)
        return redirect('docmypatient')


@login_required
def edit_patient_page(request, patient_id):
    """This is the view to load the edit patient page"""
    # Checking request method is a post ensures that this page can only
    # be accessed by navigating from the users patientPage
    if request.method == 'POST':
        # Get the patient profile details to autofill in the edit patient page with the current user's details
        patient = Profile.objects.get(id=patient_id)
        # Returns a list of doctors for the patient to be assigned to
        doctors = Doctor.objects.all()
        doctors_list = []
        for doc in doctors:
            doctors_list.append(doc)
        # Formats the DOB correctly for html
        date = patient.dob.strftime('%Y-%m-%d')
        # Returns the template with all patient and doctor details for the template to deal with
        return render(request, 'docmypatient/editPatient.html', {'patient': patient,
                                                                 'dob': date,
                                                                 'doctors': doctors_list,
                                                                 'patient_id': patient_id})
    else:
        # If the method was not a post (i.e GET) then redirect back to the main pae
        return redirect('docmypatient')


@login_required
def edit_patient(request, patient_id):
    """The post method for editing the details of the patient (POST sent from the edit patient page)"""
    # Ensures the method is a post
    if request.method == 'POST':
        # Gets the patients profile by ID
        profile = Profile.objects.get(id=patient_id)
        # Gets the patient model from the profile
        patient_profile_id = profile.patient.id
        # Retrieves all details from the POST & updates the models to match the details posted
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
        # redirects the user back to the patients Page
        return redirect('patientPage', patient_id)
    else:
        # If method is not a post then redirect back to main page
        return redirect('docmypatient')


@login_required
def delete_patient(request, patient_id):
    if request.method == 'POST':
        Profile.objects.filter(id=patient_id).delete()

    return redirect('docmypatient')


@login_required
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
                                           'patient': patient_name,
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


@login_required
def delete_comment(request, patient_id, comment_id):
    """View to handle deleting comments"""
    if request.method == 'POST':
        # Gets the comment ID from the URL <comment_id>
        comment = Comment.objects.get(id=comment_id)
        # Deletes that comment and returns a redirect back to the patients page
        comment.delete()
        return redirect('patientPage', patient_id=patient_id)
    else:
        # If method is not a post then redirect back to main page
        return redirect('docmypatient')


@login_required
def upload_file(request, patient_id):
    """This view handles uploading files and saving them to the DB"""
    if request.method == 'POST':
        # Gets the uploaded file from the POST
        uploaded_file = request.FILES['document']
        # Gets the patients name by patient_id
        patient_name = Profile.objects.get(id=patient_id)

        # Creates the uploaded file object for the model
        UploadedFile.objects.create(file_title=uploaded_file.name,
                                    staff_name=request.user.profile.user,
                                    staff_id=request.user.profile.id,
                                    patient_id=patient_id,
                                    patient = patient_name,
                                    uploaded_file=uploaded_file)

        # returns the user back to the patient page
        return redirect('patientPage', patient_id=patient_id)
    else:
        # If method is not a post then redirect back to main page
        return redirect('docmypatient')


@login_required
def download_file(request, patient_id, file_id):
    """This view handles downloading the file from the patientPage"""
    if request.method == 'POST':
        # Gets the file from models by file_id from URL <file_id> & gets file details
        file = UploadedFile.objects.get(id=file_id)
        filename = file.file_title
        # Gets the path to the file
        file_path = os.path.join(settings.MEDIA_ROOT, filename)
        # Checks that the patient id from the url matches the patient ID in the file model
        if file.patient_id != patient_id:
            raise Http404
        # If the path to the file exists send the file as a response
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                return response
        raise Http404
    else:
        return redirect('docmypatient')


@login_required
def open_comment(request, patient_id, comment_id):
    """This view handles marking the comment as open"""
    if request.method == 'POST':
        # Gets the comment by id from URL <comment_id>
        comment = Comment.objects.get(id=comment_id)
        # updates the model to True
        comment.opened = True
        comment.save()
        return redirect('patientPage', patient_id=patient_id)
    else:
        return redirect('docmypatient')


@login_required
def add_patient(request):
    """This view is for handling the creation of new patients"""
    if request.method == 'POST':
        # Checks to ensure all required details have been posted
        if request.POST.get('first_name') and request.POST.get('last_name') \
                and request.POST.get('address') and request.POST.get('ppsn'):
            # checks to see if another user with that PPSN already exists
            if check_user_exists(request.POST.get('ppsn')):
                # Creates the models objects for a patient (profile & patient model)
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
                # If an email address for the next of kin was
                # provided send an email to that person with a registration link
                # The registration link has a unique reference to the patient in it to ensure nobody else can register
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

    # Returns the template with all the doctors for selecting a doctor for the patient
    doctors = Doctor.objects.all()
    doctors_list = []
    for doc in doctors:
        doctors_list.append(doc)

    return render(request, 'docmypatient/addPatient.html', {'doctors': doctors_list})
