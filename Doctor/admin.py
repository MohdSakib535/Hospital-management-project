from django.contrib import admin
from .models import UserAccount,Appointment,PatientAdmitted,Doctor_profile,Patient_profile,Feedback,Favourite,Payment


# Register your models here.

@admin.register(UserAccount)
class UseraccountAdmin(admin.ModelAdmin):
        list_display=['id','name','email','is_doctor','is_patient',]


admin.site.register(Doctor_profile)
admin.site.register(Patient_profile)


# admin.site.register(Appointment)
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display=['id','Doctor_id','Patient_id','is_accepted_by_doctor','is_rejected_by_doctor']
# admin.site.register(AppointmentAdmin,Appointment)





@admin.register(PatientAdmitted)
class SongAdmin(admin.ModelAdmin):
    list_display=['patientId','assignedDoctor','daySpent','roomCharge','medicineCost','doctorFee','OtherCharge','Total']

# admin.site.register(PatientAdmitted)



admin.site.register(Feedback)
admin.site.register(Favourite)
admin.site.register(Payment)
