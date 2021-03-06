from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from .models import Profile
from patientZone.models import Comment
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden


def redirect_main_page(request):
    return redirect('docmypatient')


def register(request, patient_id=None):
    if request.user.is_authenticated():
        return redirect('profile')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.filter(id=patient_id).update(user=user)
            username = form.cleaned_data.get('username')
            messages.success(request, 'Your account has been successfully registered {}'.format(username))
            return redirect('profile')

        return render(request, 'users/register.html', {'form': form})

    else:
        reference = request.GET.get('reference')

        if patient_id is None or reference is None:
            return HttpResponseForbidden()
        patient_profile = Profile.objects.get(id=patient_id)

        if patient_profile.user is not None:
            return HttpResponseForbidden()

        if patient_profile.profile_reference == reference:
            form = UserRegisterForm()
        else:
            return HttpResponseForbidden()

        return render(request, 'users/register.html', {'form': form,
                                                       'patient_id': patient_id})


@login_required
def profile(request):
    if request.user.profile.is_patient:
        print("Hello")
        comments = Comment.objects.filter(patient_id=request.user.profile.id).order_by('-date_posted')
    else:
        comments = Comment.objects.filter(staff_id=request.user.profile.id).order_by('-date_posted')
    return render(request, 'users/profile.html', context={'comments': comments})
