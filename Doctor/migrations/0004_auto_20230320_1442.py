# Generated by Django 3.2.5 on 2023-03-20 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Doctor', '0003_alter_doctor_profile_likes'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='votes',
            new_name='Favourite',
        ),
        migrations.AlterField(
            model_name='doctor_profile',
            name='Description',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='doctor_profile',
            name='Languages',
            field=models.CharField(max_length=50),
        ),
    ]
