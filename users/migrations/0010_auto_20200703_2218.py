# Generated by Django 3.0.3 on 2020-07-03 22:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20200703_1958'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Doctor'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='phone_number',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='dob',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='profile',
            name='first_name',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='profile',
            name='last_name',
            field=models.CharField(max_length=30),
        ),
    ]
