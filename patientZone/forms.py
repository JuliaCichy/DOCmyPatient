from .models import Comment, UploadedFile
from users.models import Profile, Patient
from django import forms


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment', 'date_posted', 'staff_name', 'patient_id')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'dob', 'sex', 'is_patient')
