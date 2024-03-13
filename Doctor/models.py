from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser,PermissionsMixin
from django.contrib.auth.models import Group,Permission

# from django.contrib.auth.models import Permission

# credentials

# admin email :=sakib@123.com
# pass=sakib@123


class UserManager(BaseUserManager):
    def Create_user(self,email,name,is_patient=False,is_doctor=False,auth_token=None,password=None):
        email=self.normalize_email(email)
        user=self.model(email=email,name=name,is_patient=is_patient,is_doctor=is_doctor,auth_token=auth_token)
        user.set_password(password)
        # user.is_patient=True
        user.save()
        return user
    
    
    def create_superuser(self,email,name,is_doctor=False,is_patient=False,password=None):
        if(not email):
                raise ValueError("User must have an email address")

        email=self.normalize_email(email)
        user=self.model(email=email,name=name,is_doctor=is_doctor,is_patient=is_patient,)
        user.set_password(password)
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save()
        return user
    
    
class UserAccount(AbstractBaseUser,PermissionsMixin):
    email = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100,null=True,blank=True)
    is_doctor=models.BooleanField(default=False)
    auth_token=models.CharField(max_length=100)
    is_patient=models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_verified=models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects = UserManager()
    REQUIRED_FIELDS=['name']
    USERNAME_FIELD='email'

    def __str__(self):
        return f"{self.name},{self.id}"






departments=[('Cardiologist','Cardiologist'),
('Audiologists','Audiologists'),
('Cardiothoracic Surgeon','Cardiothoracic Surgeon'),
('Dentist','Dentist'),
('Endocrinologist','Endocrinologist'),
('ENT Specialists','ENT Specialists'),
('Gynecologists','Gynecologists'),
('Neurologists','Neurologists'),
('Oncologists','Oncologists'),
('Orthopedic Surgeon','Orthopedic Surgeon'),
('Pediatrician','Pediatrician'),
('Psychiatrists','Psychiatrists'),
('Pulmonologists','Pulmonologists'),
('Radiologist','Radiologist'),
('Veterinarian','Veterinarian'),
]


class Patient_profile(models.Model):
    patient_user=models.ForeignKey(UserAccount,on_delete=models.CASCADE)
    is_approved_by_doctor=models.BooleanField(default=False)
    age=models.IntegerField(null=True,blank=True)
    Gender=models.CharField(max_length=10,null=True,blank=True)
    Mobile_no=models.IntegerField(null=True,blank=True)
    Location=models.CharField(max_length=50,null=True,blank=True)
    img=models.ImageField(upload_to='myimages',null=True,blank=True)
    is_admited=models.BooleanField(default=False)
    
    
    

    def __str__(self):
        return f"{self.patient_user.name},{self.id}"


class Doctor_profile(models.Model):
    doctor_user=models.ForeignKey(UserAccount,on_delete=models.CASCADE)
    experience=models.IntegerField(null=True,blank=True)
    Qualification=models.CharField(max_length=50,blank=True,null=True)
    age=models.IntegerField(null=True,blank=True)
    Gender=models.CharField(max_length=10,null=True,blank=True)
    Speciality=models.CharField(max_length=100,choices=departments,null=True,blank=True)
    Mobile_no=models.IntegerField(null=True,blank=True)
    state=models.CharField(max_length=50,null=True,blank=True)
    city=models.CharField(max_length=50,null=True,blank=True)
    Description=models.TextField(max_length=500,null=True,blank=True)
    img=models.ImageField(upload_to='myimages',null=True,blank=True)
    fees=models.IntegerField(null=True,blank=True)
    status_by_hospital=models.BooleanField(default=False)
    joining_data=models.DateField(auto_now_add=True)
    Languages=models.CharField(max_length=50)
    likes=models.ManyToManyField(Patient_profile,null=True,blank=True)


    def __str__(self):
        return f"{self.doctor_user.name},{self.id}"
    
   

class Appointment(models.Model):
    Doctor_id=models.ForeignKey(Doctor_profile,on_delete=models.CASCADE,related_name='doctor_id')
    Patient_id=models.ForeignKey(Patient_profile,on_delete=models.CASCADE,related_name='patient_id')
    appointmentDate=models.DateTimeField()
    description=models.TextField(max_length=500)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    is_accepted_by_doctor=models.BooleanField(default=False)
    is_rejected_by_doctor=models.BooleanField(default=False)

    def __str__(self):
        return f"patient-{str(self.Patient_id.patient_user.name)},{self.id},Doctor-{str(self.Doctor_id.doctor_user.name)}"

    
   
    


class PatientAdmitted(models.Model):
    patientId=models.ForeignKey(Patient_profile,on_delete=models.CASCADE)
    assignedDoctor=models.ForeignKey(Doctor_profile,on_delete=models.CASCADE)
    symptoms = models.TextField(max_length=500,null=True,blank=True)
    admitDate=models.DateTimeField(null=True,blank=True)
    releaseDate=models.DateTimeField(null=True,blank=True)
    daySpent=models.PositiveIntegerField(null=True,blank=True)
    roomCharge=models.PositiveIntegerField(null=True,blank=True)
    medicineCost=models.PositiveIntegerField(null=True,blank=True)
    doctorFee=models.PositiveIntegerField(null=True,blank=True)
    OtherCharge=models.PositiveIntegerField(null=True,blank=True)
    Staus_by_hospital=models.BooleanField(default=False)
    status_by_doctor=models.BooleanField(default=False)
    is_discharged=models.BooleanField(default=False)

    def Total(self):
        return self.daySpent*self.roomCharge + self.medicineCost + self.doctorFee + self.OtherCharge




class Payment(models.Model):
    patient_data=models.ForeignKey(PatientAdmitted,on_delete=models.CASCADE)
    is_paid=models.BooleanField(default=False)
    razor_pay_order_id=models.CharField(max_length=200,null=True,blank=True)
    razor_pay_payment_id=models.CharField(max_length=200,null=True,blank=True)
    razor_pay_payment_signature=models.CharField(max_length=200,null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    payment_date=models.DateTimeField(null=True,blank=True)




class Feedback(models.Model):
    patient_profile_id=models.ForeignKey(Doctor_profile,on_delete=models.CASCADE)
    doctor_profile_id=models.ForeignKey(Patient_profile,on_delete=models.CASCADE)
    description=models.TextField(max_length=200)



    
class Favourite(models.Model):
    doctor_profile_data=models.ForeignKey(Doctor_profile,on_delete=models.CASCADE)
    patient_profile_data=models.ForeignKey(Patient_profile,on_delete=models.CASCADE)













