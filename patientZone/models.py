from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Comment(models.Model):

	comment = models.CharField(max_length=1000)
	date_posted = models.DateTimeField(default=timezone.now)
	show_patient = models.BooleanField(default=False)
	staff_name = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	staff_id = models.IntegerField()
	patient_id = models.IntegerField()
	patient = models.CharField(max_length=100)
	opened = models.BooleanField(default=False)

	def __str__(self):
		return self.comment
