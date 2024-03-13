# Generated by Django 4.2 on 2023-04-14 12:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Doctor', '0015_useraccount_is_verified'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('razor_pay_order_id', models.CharField(blank=True, max_length=200, null=True)),
                ('razor_pay_payment_id', models.CharField(blank=True, max_length=200, null=True)),
                ('razor_pay_payment_signature', models.CharField(blank=True, max_length=200, null=True)),
                ('patient_data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Doctor.patientadmitted')),
            ],
        ),
    ]
