# Generated by Django 3.0.3 on 2020-07-28 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patientZone', '0007_comment_show_patient'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='staff_id',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
