from django.shortcuts import render, redirect
from .models import Comments
from users.models import Patient
from django.contrib.auth.models import User
from .forms import CommentsForm
import datetime


def home(request):
    users = User.objects.all()
    users_list = []
    for user in users:
        try:
            if user.patient.doctor.id == 1:
                users_list.append(user)
        except:
            continue
    context = {
        'users': users_list
    }
    return render(request, 'docmypatient/patientZone.html', context)


def addComment(request):
    # Check if the request is a POST method
    if request.method == 'POST':
        # Get the comment and user details from the request
        nurse_comment = request.POST.get('commentData')
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        now = datetime.datetime.now()

        # Post to the comments form
        comments_form = CommentsForm(data={'nurse_comment': nurse_comment,
                                           'date_posted': now,
                                           'nurse_name': user})
        # Check if its vaild
        if comments_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comments_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.nurse_comment = nurse_comment
            new_comment.nurse_name = user
            # Save the comment to the database
            new_comment.save()
            return redirect('docmypatient')
        else:
            return redirect('docmypatient')

    else:
        return redirect('docmypatient')

