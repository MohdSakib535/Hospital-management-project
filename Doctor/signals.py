from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import UserAccount,Doctor_profile,Patient_profile

@receiver(post_save,sender=UserAccount)
def Save_profile(sender,instance,created,**kwargs):
    if created:
        if instance.is_doctor:
           Doctor_profile.objects.create(doctor_user=instance)
        else:
           Patient_profile.objects.create(patient_user=instance,)
 

        # print('----------',instance)
        # print('----n------',instance.name)