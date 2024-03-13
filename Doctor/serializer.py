from .models import UserAccount,Patient_profile,Doctor_profile,PatientAdmitted,Payment,Appointment
from rest_framework import serializers

class User_Account_serializer(serializers.ModelSerializer):
    class Meta:
        model=UserAccount
        fields='__all__'


class Patient_Profile_serializer(serializers.ModelSerializer):
    class Meta:
        model=Patient_profile
        fields='__all__'


class Doctor_Profile_serializer(serializers.ModelSerializer):
    doctor_user=User_Account_serializer()
    class Meta:
        model=Doctor_profile
        fields=['id','experience','Qualification','age','Gender','Speciality','Mobile_no','state','city','Description','img','fees','status_by_hospital','joining_data','Languages','doctor_user','likes']


class Appointment_serializer(serializers.ModelSerializer):
    Doctor_id=Doctor_Profile_serializer()
    # doctor_name = serializers.StringRelatedField(source='Doctor_id.doctor_user.name')


    # Patient_id=Patient_Profile_serializer()
    #     or
    Patient_name = serializers.StringRelatedField(source='Patient_id.patient_user.name')

    class Meta:
        model=Appointment
        fields=['id','appointmentDate','description','created_at','is_accepted_by_doctor','is_rejected_by_doctor','Doctor_id','Patient_name']


class Patient_Admitted_serializer(serializers.ModelSerializer):
    class Meta:
        model=PatientAdmitted
        fields='__all__'


class Payment_serializer(serializers.ModelSerializer):
    class Meta:
        model=Payment
        fields='__all__'