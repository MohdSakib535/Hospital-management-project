# Generated by Django 4.2 on 2023-04-15 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Doctor', '0017_alter_payment_patient_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='is_paid',
            field=models.BooleanField(default=False),
        ),
    ]
