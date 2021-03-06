# Generated by Django 3.0.3 on 2020-07-29 16:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('patientZone', '0009_comment_patient'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadedFiles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(max_length=10000)),
                ('patient_id', models.IntegerField()),
                ('staff_id', models.IntegerField()),
                ('patient', models.CharField(max_length=100)),
                ('uploaded_file', models.FileField(upload_to='uploaded_files/')),
                ('staff_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
