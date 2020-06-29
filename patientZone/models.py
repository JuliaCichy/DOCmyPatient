from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Comment(models.Model):

	comment = models.CharField(max_length=1000)
	date_posted = models.DateTimeField(default=timezone.now)
	staff_name = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	patient_id = models.IntegerField()
	opened = models.BooleanField(default=False)

	def __str__(self):
		return self.comment
