# Generated by Django 4.2 on 2023-04-15 09:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Doctor', '0019_alter_payment_patient_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='patient_data',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Doctor.patientadmitted'),
        ),
    ]
