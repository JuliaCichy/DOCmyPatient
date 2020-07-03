# Generated by Django 3.0.3 on 2020-07-03 19:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0007_auto_20200703_1932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='profile',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.Profile'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='sex',
            field=models.CharField(choices=[('F', 'Female'), ('M', 'Male'), ('O', 'Other')], max_length=1),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
