# Generated by Django 3.2.5 on 2023-03-17 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Doctor', '0002_doctor_profile_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor_profile',
            name='likes',
            field=models.ManyToManyField(blank=True, null=True, to='Doctor.Patient_profile'),
        ),
    ]
