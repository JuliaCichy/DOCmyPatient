from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Comments(models.Model):

    nurse_comment = models.CharField(max_length=1000)
    date_posted = models.DateTimeField(default=timezone.now)
    nurse_name = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.nurse_comment

