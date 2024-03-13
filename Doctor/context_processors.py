from .models import Doctor_profile,UserAccount,Patient_profile
from django.db.models import Q
import datetime





def user_data(request):
    doctor_data=Doctor_profile.objects.filter(doctor_user_id=request.user.id)
    # print('data---------',doctor_data)
    patient_data=Patient_profile.objects.filter(patient_user_id=request.user.id)
    # print('data---------',patient_data)
   
    return {'current_year': datetime.datetime.now().year,
            'doctor_data':doctor_data,
            'patient_data':patient_data,
            
            }
    