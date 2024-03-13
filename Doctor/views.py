from django.shortcuts import render,redirect
from .models import *
from .task import *
from django.contrib.auth import login,logout,authenticate 
from django.conf import settings
from django.core.files import File
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse,HttpResponse
from datetime import datetime
from django.db.models import Q
from datetime import datetime,timedelta
from django.db import connection
import uuid
import json
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.core.cache import cache
import razorpay
from django.contrib import messages
from .utils import render_to_pdf
from django.contrib.auth.decorators import login_required



CACHE_TTL=getattr(settings,'CACHE_TTL',DEFAULT_TIMEOUT)

# Create your views here.
def home(request):
    messages.add_message(request, messages.SUCCESS,
                             "welcome to webpage")
    return render(request,'homepage/home.html')


def about(request):
    return render(request,'homepage/about.html')


def Registraton(request):
    if request.method=='POST':
        user_type=request.POST['data']
        auth_token=str(uuid.uuid4())
        print('---------',user_type)
        if user_type=='patient':
            name=request.POST['name']
            email=request.POST['email']
            age=request.POST['age']
            gender=request.POST.get('gender-select')
            mobile=request.POST['mobile']
            location=request.POST.get('location',None)
            img=request.FILES.get('file-img',None)
            print('img-----------',img)
            password=request.POST['password']
            repassword=request.POST['repassword']

            if UserAccount.objects.filter(email=email).exists():
                messages.add_message(request, messages.SUCCESS,
                             "email already exist")
                return redirect('registration')
            if password == repassword:
                
                registered_user=UserAccount.objects.Create_user(name=name,email=email,is_patient=True,password=password,auth_token=auth_token)
                registered_user.save()

                patient_profile_data=Patient_profile.objects.get(patient_user_id=registered_user.id)
                patient_profile_data.age=age
                patient_profile_data.Gender=gender
                patient_profile_data.Mobile_no=mobile
                patient_profile_data.Location=location
                patient_profile_data.img=img
                patient_profile_data.save()


                send_mail_task_with_celery.delay('Account need to verify',email,f"hi paste to verify account http://127.0.0.1:8000/verify-token/{auth_token}")
                return redirect('token_send')
            else:
                messages.add_message(request, messages.SUCCESS,
                             "password not matched")
                
        else:
            if user_type=='doctor':
                name=request.POST.get('name',None)
                print(name)
                email=request.POST['email']
                age=request.POST['age']
                gender=request.POST.get('gender-select')
                speciality=request.POST.get('speciality')
                mobile=request.POST['mobile']
                experience=request.POST.get('experience',None)
                state=request.POST.get('state',None)
                fees=request.POST.get('fees',None)
                city=request.POST.get('city',None)
                description=request.POST.get('description',None)
                img=request.FILES.get('file-img',None)
                print('--img----',img)
                password=request.POST['password']
                repassword=request.POST['repassword']

                if UserAccount.objects.filter(email=email).exists():
                    messages.add_message(request, messages.SUCCESS,
                             "email already exist")
                    return redirect('registration')
                if password==repassword:
                    registered_user1=UserAccount.objects.Create_user(name=name,email=email,is_doctor=True,password=password,auth_token=auth_token)
                    registered_user1.is_active=True
                    registered_user1.save()
                    
                    print('---r---',registered_user1.id)
                    doctor_profile_data=Doctor_profile.objects.get(doctor_user_id=registered_user1.id)
                    doctor_profile_data.Gender=gender
                    doctor_profile_data.age=age
                    doctor_profile_data.Speciality=speciality
                    doctor_profile_data.Mobile_no=mobile
                    doctor_profile_data.experience=experience
                    doctor_profile_data.state=state
                    doctor_profile_data.fees=fees
                    doctor_profile_data.city=city
                    doctor_profile_data.Description=description
                    doctor_profile_data.img=img
                    doctor_profile_data.save()
                    # return redirect('token_send')
                    send_mail_task_with_celery.delay('Account need to verify',email,f"hi paste to verify account http://127.0.0.1:8000/verify-token/{auth_token}")
                    return redirect('token_send')
                else:
                    messages.add_message(request, messages.SUCCESS,
                             "email already exist")
    return render(request,'homepage/registration.html')


def Token_Send(request):
    return render(request,'homepage/token_send.html')

def Forget_password(request):
    if request.method == "POST":
        email=request.POST['email']
        check_email_data=UserAccount.objects.filter(email=email).first()
        if check_email_data:
            print('---em---',check_email_data)
            print('------',check_email_data.auth_token)
            auth_token=check_email_data.auth_token
            send_mail_task_with_celery.delay('Forget Password',email,f"hi paste to verify account http://127.0.0.1:8000/change-password/{auth_token}")
            return redirect('token_send')
        else:
            messages.add_message(request, messages.WARNING,
                             "Email does not exist")



    return render(request,'homepage/forget_password.html')

def Change_password(request,auth_token):
    user_obj=UserAccount.objects.filter(auth_token=auth_token).first()
    if request.method=="POST":
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']
        if password != confirm_password:
            messages.add_message(request, messages.SUCCESS,
                             "password not match")
        user_obj.set_password(confirm_password)
        user_obj.save()
        return redirect('login')
    return render(request,'homepage/change_password.html')

def Verify_token(request,auth_token):
    verify_token_data=UserAccount.objects.filter(auth_token=auth_token).first()
    print('verify_data token-------------',verify_token_data)
    print('verify_data token-------------',verify_token_data.is_verified)
    if verify_token_data:
        if verify_token_data.is_verified:
            messages.add_message(request, messages.SUCCESS,
                             "user already verified")
        else:
            verify_token_data.is_verified=True
            verify_token_data.is_active=True
            verify_token_data.save()


    return redirect('login')

def Login(request):
    if request.method=='POST':
        email=request.POST['email']
        # print('----',email)
        password=request.POST['password']
        # print('---',password)
        user = authenticate(email=email,password=password)
        # print('--cd----',user)
        if user:
            login(request, user)
            messages.add_message(request, messages.SUCCESS,
                             "login in sucessful")
            
            return redirect('home')
        else:
            messages.add_message(request, messages.WARNING,
                             "Login credentials wrong check again")
    

    return render(request,'homepage/login.html')

@login_required(login_url='/')
def Profile(request):
    if request.method == "POST":
        type=request.POST['type']
        if type == 'doctor':
            id=request.POST.get('id')
            # img=request.POST['img']
            name=request.POST.get('name')
            qualification=request.POST['qualification']
            speciality=request.POST['speciality']
            state=request.POST['state']
            city=request.POST['city']
            experience=request.POST['experience']
            mobile=request.POST['mobile']
            age=request.POST['age']
            fees=request.POST['fees']
            gender=request.POST['gender']
            language=request.POST['language']
            description=request.POST.get('description')

            update_data_details=Doctor_profile.objects.filter(id=id).first()

            update_data_details.Qualification=qualification
            update_data_details.Speciality=speciality
            update_data_details.state=state
            update_data_details.city=city
            update_data_details.experience=experience
            update_data_details.Mobile_no=mobile
            # update_data_details.img=img
            update_data_details.fees=fees
            update_data_details.Gender=gender
            update_data_details.Languages=language
            update_data_details.Description=description
            update_data_details.age=age
            update_data_details.save()
            update_data_details.doctor_user.name=name
            update_data_details.doctor_user.save()
            return redirect('profile')
        else:
            id=request.POST['id']
            name=request.POST['name']
            print('name---',name)
            location=request.POST['location']
            print('----l--',location)
            mobile=request.POST['mobile']
            gender=request.POST['gender']
            age=request.POST['age']
            update_patient_details=Patient_profile.objects.filter(id=id).first()
            update_patient_details.Location=location
            update_patient_details.Mobile_no=mobile
            update_patient_details.Gender=gender
            update_patient_details.age=age
            update_patient_details.patient_user.name=name
            update_patient_details.save()
            update_patient_details.patient_user.save()
            return redirect('profile')

            
        # return render(request,'dashboard/edit_profile.html')
    else:

        if request.user.is_doctor:
            curr_doctor_data=Doctor_profile.objects.prefetch_related('doctor_user').filter(doctor_user_id=request.user.id)
            print('c---------',curr_doctor_data)
        
        else:
            curr_doctor_data=Patient_profile.objects.prefetch_related('patient_user').filter(patient_user_id=request.user.id)
            print('p---------', curr_doctor_data)

        return render(request,'dashboard/profile.html',context={'curr_profile':curr_doctor_data})


def Doctor_logout(request):
    logout(request)
    return redirect('home')

def tables(request):
    return render(request,'dashboard/tables1.html')

def Index(request):
    return render(request,'dashboard/index.html')


def All_patient_data(user):
    patient_user_data=user
    print('patient_user----',patient_user_data)

    # patient_profile_data=Patient_profile.objects.get(patient_user=patient_user)
    # print('patient_profile_data----',patient_profile_data)

    # appointment_data=Appointment.objects.filter(Patient_id=patient_profile_data  ).count()
    # print('appointment_data----',appointment_data)

    # or
    
    appointment_data=Appointment.objects.select_related('Patient_id__patient_user').filter(Patient_id__patient_user=patient_user_data).count()
    # print('---d2-----------',appointment_data)
    fav=Favourite.objects.select_related('patient_profile_data__patient_user').filter(patient_profile_data__patient_user=user).count()

    all_data=[appointment_data,fav]
    
    return  all_data


def All_doctor_Data(user):
    doctor_user_data=user
    print('patient_user----',doctor_user_data)
    appointment_Dta=Appointment.objects.select_related('Doctor_id__doctor_user').filter(Doctor_id__doctor_user=doctor_user_data).count()
    print('appointment_Dta----',appointment_Dta)
    return appointment_Dta


    




@login_required(login_url='/')
def Dashboard(request):
    patient_appointment_data=All_patient_data(request.user)
    doctor_appointment=All_doctor_Data(request.user)

    total_doctors=Doctor_profile.objects.filter(status_by_hospital=True).count()
    total_patient=Patient_profile.objects.all().count()
    total_appointment=Appointment.objects.all().count()
    total_patient_discharge=PatientAdmitted.objects.filter(is_discharged=True).count()
    print('------',total_doctors)
    context_data={'doctor':total_doctors,
                  'patient':total_patient,
                  'appointment':total_appointment,
                  'total_patient_discharge':total_patient_discharge,
                  'patient_appointment_data':patient_appointment_data,
                  'doctor_appointment':doctor_appointment
                  
                  
                  
                  }


    return render(request,'dashboard/dashboard.html',context=context_data)


@login_required(login_url='/')
@csrf_exempt
def New_Doctor_Data(request):
    if request.method=="POST":
        id=request.POST['id']
        print(id)
        value=request.POST['value']
        print(value)
        if value=='Accept':
            doctor_data=Doctor_profile.objects.get(id=id)
            doctor_data.status_by_hospital=True
            doctor_data.save()

            return JsonResponse({'status':'accept'})
        else:
            pass

    else:    
        registered_doctor_data=Doctor_profile.objects.filter(status_by_hospital=False)
        print(registered_doctor_data)
    return render(request,'dashboard/new_doctor_data.html',context={'data':registered_doctor_data})



@login_required(login_url='/')
def Approved_Doctor_Data(request):
    approved_doctor_data=Doctor_profile.objects.filter(status_by_hospital=True).all()
    print(approved_doctor_data)
    return render(request,'dashboard/approved_doctor_data.html',context={'data':approved_doctor_data})


@login_required(login_url='/')
def Patient_Data(request):
    patient_data=Patient_profile.objects.all()

    return render(request,'dashboard/all_patients.html',context={'data':patient_data})


@login_required(login_url='/')
def Search_Doctor(request):
    patient_profile_id_data=Patient_profile.objects.get(patient_user_id=request.user.id)
    print('---s3-----',patient_profile_id_data.id)
    appointment_date=''
    if request.method=="POST":
        date_data=request.POST['Date_Data4']
        dt = datetime.fromisoformat(str(date_data))
        formatted_dt = dt.strftime('%Y-%m-%d %H:%M:%S')
        # print('formatted_dt--------',formatted_dt)
        text_description=request.POST.get('patient_symptoms')
        # print('d-------',text_description)
        doctor_id=request.POST['doctor_id']
        appointment_date=Appointment.objects.create(Doctor_id=Doctor_profile.objects.get(id=doctor_id),Patient_id=Patient_profile.objects.get(id=patient_profile_id_data.id),appointmentDate=formatted_dt,description=text_description)
        appointment_date.save()
    
    doctor_details=Doctor_profile.objects.filter(status_by_hospital=True).order_by('fees')
    # print('----dd2--',doctor_details)
    like_count=[]
    check_patient_id=[]
    fav_dta=[]
    for data in doctor_details:
        # print(i.likes.all())
        like_count.append(data.likes.all().count())
        check_patient_id.append(data.likes.filter(id=patient_profile_id_data.id))
        Favourite_data=Favourite.objects.filter(doctor_profile_data_id=data.id,patient_profile_data_id=patient_profile_id_data.id)
        fav_dta.append(Favourite_data)
    content_data=list(zip(doctor_details,like_count,check_patient_id,fav_dta))

    return render(request,'dashboard/search_doctor_page.html',context={'doctor_details':content_data,'patient_profile_id':patient_profile_id_data.id})



@login_required(login_url='/')
def Search_Doctor_name(request):
    patient_profile_id_data = Patient_profile.objects.get(patient_user_id=request.user.id)
    content_data2 = ''

    if request.method == 'POST':
        doctor_name = request.POST.get('search')
        # print('-dn--', doctor_name)

        cache_key = f'doctor_details_{doctor_name}'
        print('cache_key--------',cache_key)
        doctor_details = cache.get(cache_key)
        print('doctr_detail----------',doctor_details)
        

        if doctor_details is None:
            print('data from database')
            # print(connection.queries)  
            doctor_details = Doctor_profile.objects.prefetch_related('doctor_user').filter(doctor_user__name=doctor_name)
            cache.set(cache_key, doctor_details)
        else:
            print('data from cache')
            # print(connection.queries)  

        like_count = []
        check_patient_id = []
        fav_dta = []

        for data in doctor_details:
            like_count.append(data.likes.all().count())
            check_patient_id.append(data.likes.filter(id=patient_profile_id_data.id))
            Favourite_data = Favourite.objects.filter(doctor_profile_data_id=data.id, patient_profile_data_id=patient_profile_id_data.id)
            fav_dta.append(Favourite_data)

        content_data2 = list(zip(doctor_details, like_count, check_patient_id, fav_dta))

    return render(request, 'dashboard/search_doctor_name.html', context={'doctor_details': content_data2, 'patient_profile_id': patient_profile_id_data.id})


# def Search_Doctor_name(request):
#     patient_profile_id_data=Patient_profile.objects.get(patient_user_id=request.user.id)
#     content_data2=''
#     if request.method=='POST':
#         doctor_name=request.POST.get('search')
#         print('-dn--',doctor_name)

#         doctor_details=Doctor_profile.objects.prefetch_related('doctor_user').filter(doctor_user__name=doctor_name)
#         # print('search_data3----------------',doctor_details)
#         like_count=[]
#         check_patient_id=[]
#         fav_dta=[]
#         for data in doctor_details:
#             # print(i.likes.all())
#             like_count.append(data.likes.all().count())
#             check_patient_id.append(data.likes.filter(id=patient_profile_id_data.id))
#             Favourite_data=Favourite.objects.filter(doctor_profile_data_id=data.id,patient_profile_data_id=patient_profile_id_data.id)
#             fav_dta.append(Favourite_data)
#         content_data2=list(zip(doctor_details,like_count,check_patient_id,fav_dta))
    
#     return render(request,'dashboard/search_doctor_name.html',context={'doctor_details':content_data2,'patient_profile_id':patient_profile_id_data.id})


@login_required(login_url='/')
def Filtered_doctor_data(request):
    patient_profile_id_data=Patient_profile.objects.get(patient_user_id=request.user.id)
    # doctor_details=''
    # specialist_data=''
    # gender_data=''
    # state_data=''
    # experience_data=''
    
    if request.method=="GET":
        specialist_data=request.GET.get('select-specialist',None)
        # print('sp----------',specialist_data)
        gender_data=request.GET.get('select-gender',None)
        print('g----------',gender_data)
        state_data=request.GET.get('select-state',None)
        # print('state----------',state_data)
        experience_data=request.GET.get('select-experience',None)
        # print('e----------',experience_data)


        if specialist_data:
            doctor_details=Doctor_profile.objects.filter(Speciality=specialist_data).all()
            if gender_data :
                doctor_details=doctor_details.filter(Gender__iexact=gender_data).all()
            else:
                pass
            if state_data :
                doctor_details=doctor_details.filter(state__iexact=state_data).all()
            else:
                pass
            if experience_data:
                if experience_data=='young':
                    doctor_details=doctor_details.filter(experience__lte=20).all()
                elif experience_data=='old':
                    doctor_details=doctor_details.filter(experience__gte=20).all() 
                else:
                    pass

        elif gender_data:
            doctor_details=Doctor_profile.objects.filter(Gender__iexact=gender_data).all()
            # print('gender_details---------',doctor_details)
           
            if state_data :
                doctor_details=doctor_details.filter(state__iexact=state_data).all()
            else:
                pass
            if experience_data=='young':
                doctor_details=doctor_details.filter(experience__lte=20)
            elif experience_data=='old':
                doctor_details=doctor_details.filter(experience__gte=20)
            else:
                pass

        elif state_data:
            doctor_details=Doctor_profile.objects.filter(state__iexact=state_data)
            # print('state_d---------',doctor_details)
            if experience_data=='young':
                doctor_details=doctor_details.filter(experience__lte=20).all()
            elif experience_data=='old':
                doctor_details=doctor_details.filter(experience__gte=20)
            else:
                pass

        elif experience_data:
            if experience_data=='young':
               doctor_details=Doctor_profile.objects.filter(experience__lte=20).all()
            else:
               doctor_details=Doctor_profile.objects.filter(experience__gte=20).all() 
        else:
            print('click at least')  
        
            # print('dd---------',doctor_details)

        like_count=[]
        check_patient_id=[]
        fav_dta=[]
        for data in doctor_details:
            like_count.append(data.likes.all().count()) 
            check_patient_id.append(data.likes.filter(id=patient_profile_id_data.id))
            Favourite_data=Favourite.objects.filter(doctor_profile_data_id=data.id,patient_profile_data_id=patient_profile_id_data.id)
            fav_dta.append(Favourite_data)
        content_data=list(zip(doctor_details,like_count,check_patient_id,fav_dta))
        # print('cd----------',content_data)
      
    else:
        doctor_details=Doctor_profile.objects.filter(Q(Speciality=specialist_data) | Q(Gender__iexact=gender_data) | Q(state__iexact=state_data) & Q(status_by_hospital=True)).all()
        # print('l4-----',doctor_details)
        like_count=[]
        check_patient_id=[]
        fav_dta=[]
        for i in doctor_details:
            like_count.append(i.likes.all().count()) 
            check_patient_id.append(i.likes.filter(id=patient_profile_id_data.id))
            Favourite_data=Favourite.objects.filter(doctor_profile_data_id=data.id,patient_profile_data_id=patient_profile_id_data.id)
            fav_dta.append(Favourite_data)
        content_data=list(zip(doctor_details,like_count,check_patient_id,fav_dta))

       


    # return render(request,'dashboard/search_doctor_page.html',context={'doctor_details':content_data,'patient_profile_id':patient_profile_id_data.id,})
    return render(request,'dashboard/filter_doctor.html',context={'doctor_details':content_data,'patient_profile_id':patient_profile_id_data.id,'edit_data':doctor_details})
    

@login_required(login_url='/')
def Doctor_Response_Data(request):
    # doctor_name=request.GET.get('search')
    # print('---',doctor_name)
    search_data=Doctor_profile.objects.prefetch_related('doctor_user').all()
    # print('---',search_data)
    if search_data:
        data=[]
        for i in search_data:
            # print(i.doctor_user.name)
            data.append(i.doctor_user.name)
        # print('---',data)
        # return JsonResponse(data,safe=False)

        return JsonResponse({'data':data,'status':'success'})
    # return redirect('search_doctor')
  

@login_required(login_url='/')
def Appointment_Data(request):
    if request.method=="POST":
        new_date=request.POST['Date_Data']
        dt = datetime.fromisoformat(str(new_date))
        formatted_new_date = dt.strftime('%Y-%m-%d %H:%M:%S')
        # patient_id_values=request.POST.get('patient_id_value')
        appointment_id=request.POST.get('appointment_id')
        # print('patient-------',patient_id_values)
        Appointment.objects.filter(id=appointment_id).update(appointmentDate=formatted_new_date)
    
        
    #or

        # update_date=Appointment.objects.filter(Patient_id_id=patient_id_values)
        # print('update_data----',update_date)
        
        # for i in update_date:
        #     i.appointmentDate=formatted_dt
        #     i.save()
    
    show_patient_data=Patient_profile.objects.get(patient_user_id=request.user.id)
    appointment_dta=Appointment.objects.filter(Patient_id_id=show_patient_data.id).order_by('-created_at')
    print('----app dta---',appointment_dta)
    return render(request,'dashboard/appointment.html',context={'appointment_data':appointment_dta})


@login_required(login_url='/')
@csrf_exempt
def Doctor_Appointment(request):
    if request.method=="POST":
        id=request.POST['appointment_id']
        # print('-------',id)

        patinet_id=request.POST['patient_id']
        # print('-----pid-----',patinet_id)

        doctor_id=request.POST['doctor_id']
        # print('-----did-----',doctor_id)

        value=request.POST['value']
        print(value)

        form_data=request.POST.get('description_data',None)
        # print('form-----------',form_data)

        if value=='Accept':
            appointment_data=Appointment.objects.get(id=id)
            appointment_data.is_accepted_by_doctor=True
            appointment_data.save()
            return JsonResponse({'status':'accept'})
        elif value == "Reject":
            reject_data=Appointment.objects.get(id=id)
            reject_data.is_rejected_by_doctor=True
            reject_data.save()
            return JsonResponse({'status':'reject'})
        else:
            patient_profile_data=Patient_profile.objects.get(id=patinet_id)
            patient_profile_data.is_admited=True
            patient_profile_data.save()
            
            
            now=datetime.now()
            print('---n-------',now)
            dt = datetime.fromisoformat(str(now))
            formatted_dt = dt.strftime('%Y-%m-%d %H:%M:%S')
            print('formatted_dt--------',formatted_dt)


            admitted_data=PatientAdmitted(patientId_id=patinet_id,assignedDoctor_id=doctor_id,admitDate=formatted_dt,symptoms=form_data)
            admitted_data.save()
            print('pprofieke-----------------',patient_profile_data)
            print('admitted')
            return JsonResponse({'status':'admit'})
        
       
    else:

        show_doctor_data=Doctor_profile.objects.get(doctor_user_id=request.user.id)
        appointment_dta=Appointment.objects.filter(Doctor_id_id=show_doctor_data.id).order_by('-created_at')
    return render(request,'dashboard/doctorAppointment.html',context={'appointment_data':appointment_dta})


@login_required(login_url='/')
@csrf_exempt
def Appointment_Delete(request):
    if request.method=="POST":
        id=request.POST.get('id')
        # print('-----',btn_value,id)
    delete_appointment=Appointment.objects.get(id=id)
   
    delete_appointment.delete()
    return JsonResponse({'status':'deleted'})


# @csrf_exempt
# def Doctor_votes(request):
#     if request.method=="POST":
#         patient_profile_id=request.POST.get('patient_id')
#         doctor_profile_id=request.POST.get('doctor_id')
#         # print('----------------',patient_profile_id,doctor_profile_id)
#         data=request.POST.get('value')
#         print('value---------',data)


#         check_patient_profile=Patient_profile.objects.get(id=patient_profile_id)
#         # print('---c----',check_patient_profile)

#         check_doctor_profile=Doctor_profile.objects.get(id=doctor_profile_id)


#         check_id_exist=Doctor_profile.objects.filter(likes=check_patient_profile)
#         # print('-----cid--',check_id_exist)
#         if check_id_exist.exists() :
#             check_doctor_profile.likes.remove(check_patient_profile)
#             counting=Doctor_profile.objects.get(id=doctor_profile_id)
#             like_count=counting.likes.all().count()
#             return JsonResponse({'status':'unlike','count':like_count})

#         else:
#             check_doctor_profile.likes.add(check_patient_profile)
#             counting=Doctor_profile.objects.get(id=doctor_profile_id)
#             like_count=counting.likes.all().count()
#             return JsonResponse({'status':'like','count':like_count})
        

@login_required(login_url='/')
@csrf_exempt
def Doctor_votes(request):
    if request.method=="POST":
        patient_profile_id=request.POST.get('patient_id')
        doctor_profile_id=request.POST.get('doctor_id')
        # print('----------------',patient_profile_id,doctor_profile_id)
        data=request.POST.get('value')
        print('value---------',data)

        check_patient_profile=Patient_profile.objects.get(id=patient_profile_id)
        print('---c----',check_patient_profile)

        check_doctor_profile=Doctor_profile.objects.get(id=doctor_profile_id)
        print('dp---------',check_doctor_profile)
        if data=='like':
            check_doctor_profile.likes.add(check_patient_profile)
            counting=Doctor_profile.objects.get(id=doctor_profile_id)
            like_count=counting.likes.all().count()
            return JsonResponse({'status':'like','count':like_count})
        else:
            check_doctor_profile.likes.remove(check_patient_profile)
            counting=Doctor_profile.objects.get(id=doctor_profile_id)
            like_count=counting.likes.all().count()
            print('lc-----',like_count)
            return JsonResponse({'status':'unlike','count':like_count})


@login_required(login_url='/')
@csrf_exempt
def Favourite_Doctor_Data(request):
    patient_profile_id_data=Patient_profile.objects.get(patient_user_id=request.user.id)
    content_data=''
    if request.method=="POST":
        patient_profile_id=request.POST.get('patient_id')
        doctor_profile_id=request.POST.get('doctor_id')
        value_data=request.POST.get('value_data')
        g2=Favourite.objects.filter(patient_profile_data=patient_profile_id,doctor_profile_data=doctor_profile_id)
        # print('g2-------------',g2)
        if value_data=='bookmark':
            if not g2 :
                s2=Favourite.objects.create(patient_profile_data=Patient_profile.objects.get(id=patient_profile_id),doctor_profile_data=Doctor_profile.objects.get(id=doctor_profile_id))
                s2.save()
                return JsonResponse({'status':'success'})
            else:
                print('data is already present')
                return JsonResponse({'status':'Already_present'})
        else:
            fav_delete=Favourite.objects.get(id=value_data)
            fav_delete.delete()
            return JsonResponse({'status':'delete'})
        


    print('-------',patient_profile_id_data)
    fav_data=Favourite.objects.filter(patient_profile_data=patient_profile_id_data).all()
    print('---fav----------------',fav_data)
    # for i in fav_data:
    #     if i.patient_profile_data=

    like_count=[]
    for data in fav_data:
        # print('---l--',data.doctor_profile_data.likes.all())
        like_count.append(data.doctor_profile_data.likes.all().count())
        print('---like------c----',like_count)
        # check_patient_id.append(data.likes.filter(id=patient_profile_id_data.id))
    content_data=list(zip(fav_data,like_count))
    print('----c----------',content_data)
    
    # return render(request,'dashboard/favourite_doctor.html',context={'favourite':content_data,'p':patient_profile_id_data,'d':doctor_profile_id})
    return render(request,'dashboard/favourite_doctor.html',context={'favourite':content_data})


@login_required(login_url='/')
def Payments_data(request):
    patient_profile_id_data=Patient_profile.objects.get(patient_user_id=request.user.id)
    # d6=PatientAdmitted.objects.get(id=)
    payment_data_profile=PatientAdmitted.objects.filter(patientId_id=patient_profile_id_data, Staus_by_hospital=True).all()
    print('--pp----',payment_data_profile)
    l=[]
    for i in payment_data_profile:
        print('-------',i.patientId)
        check_payment_data=Payment.objects.filter(patient_data=i.id).order_by('-created_at').first()
        print('ckeck_payment-------------------',check_payment_data)
        # for k in check_payment_data:
        #     print('---k--------------',k)

        l.append(check_payment_data)
       
    contxt=list(zip(payment_data_profile,l))
    print('c------',contxt)

    return render(request,'dashboard/payment.html',context={'paymet_data':contxt})



@login_required(login_url='/')
def Invoice_Data(request,id):
    print('id------------',id)
    patient_profile_data2=PatientAdmitted.objects.filter(id=id)

    l=[]
    for i in patient_profile_data2:

        client = razorpay.Client(auth=(settings.ID, settings.SECRET ))
        data = {"amount":(i.Total()-200)*100, "currency": "INR", "receipt": "order_rcptid_11"}
        payment = client.order.create(data=data)
        patient_profile_data=PatientAdmitted.objects.filter(id=id).first()
        print('pa-----------',patient_profile_data)

        payment_data=Payment.objects.create(patient_data=patient_profile_data,razor_pay_order_id=payment['id'],payment_date=datetime.now())
        payment_data.save()
        print("*******")
        print(payment)
        print("*******")

        print('-------',i.patientId)
        # check_payment_data=Payment.objects.filter(patient_data=i.id).all().order_by('-created_at').first()
        check_payment_data=Payment.objects.filter(patient_data=i.id).latest('created_at')
        print('ckeck_payment-------------------',check_payment_data)

        # for k in check_payment_data:
        #     print('---k--------------',k)

        l.append(check_payment_data)

    contxt=list(zip(patient_profile_data2,l))
    print('c------',contxt)
    return render(request,'dashboard/invoice_data.html',context={'payment':payment,'patient_profile_data2':contxt})
        


@login_required(login_url='/')
def Invoice_Data_Download(request,id):
    patient_profile_data2=PatientAdmitted.objects.filter(id=id)
    l=[]
    for i in patient_profile_data2:
        check_payment_data=Payment.objects.filter(patient_data=i.id).latest('created_at')
        print('ckeck_payment-------------------',check_payment_data)

        # for k in check_payment_data:
        #     print('---k--------------',k)

        l.append(check_payment_data)

    contxt=list(zip(patient_profile_data2,l))
    print('c------',contxt)

    pdf = render_to_pdf('dashboard/invoice_data_download.html', context={'patient_profile_data2':contxt})
    return HttpResponse(pdf, content_type='application/pdf')
  

    # return render(request,'dashboard/invoice_data_download.html',context={'patient_profile_data2':contxt})






@login_required(login_url='/')
def Payment_success(request):
    order_id=request.GET.get('order_id')
    print('order_id--------------',order_id)
    
    razorpay_order_id=request.GET.get('razorpay_order_id')
    print('razorpay_order_id--------------',razorpay_order_id)

    razorpay_payment_id=request.GET.get('razorpay_payment_id')
    print('razorpay_payment_id--------------',razorpay_payment_id)

    razorpay_signature=request.GET.get('razorpay_signature')
    print('razorpay_signature--------------',razorpay_signature)

    check_order_id=Payment.objects.get(razor_pay_order_id=order_id)

    check_order_id.razor_pay_order_id=razorpay_order_id
    check_order_id.razor_pay_payment_id=razorpay_payment_id
    check_order_id.razor_pay_payment_signature=razorpay_signature

    check_order_id.is_paid=True
    check_order_id.save()
    # return HttpResponse('payment success')
    return render(request,'dashboard/payment_success.html',context={'order_id':order_id})



@login_required(login_url='/')
@csrf_exempt
def Admitted_Data_List(request):
    show_doctor_data=Doctor_profile.objects.get(doctor_user_id=request.user.id)
    print(show_doctor_data)
    if request.method=="POST":
        patient_id=request.POST['patient_id']
        print('--pid----',patient_id)
        now=datetime.now()
        print('---n-------',now)
        days_later=now + timedelta(days=2)
        dt = datetime.fromisoformat(str(days_later))
        # dt = datetime.fromisoformat(str(now))
        formatted_dt = dt.strftime('%Y-%m-%d %H:%M:%S')
        print('formatted_dt--------',formatted_dt)

        PatientAdmitted.objects.filter(assignedDoctor_id=show_doctor_data).update(releaseDate=formatted_dt,status_by_doctor=True)
        
        
        return JsonResponse({'status':'discharge'})
        



    
    admited_patient_profile=PatientAdmitted.objects.filter(assignedDoctor_id=show_doctor_data.id).order_by('-admitDate')
    # print('---ad------',admited_patient_profile)
    return render(request,'dashboard/doctor_admitted_data.html',context={'admitted_patient_data':admited_patient_profile})   


# @csrf_exempt
# def Admit_data(request):
#     if request.method=="POST":
#         id=request.POST['id']
#         print('-------',id)
#         patinet_id=request.POST['p_id']
#         print('-----pid-----',patinet_id)
#         doctor_id=request.POST['d_id']
#         print('-----did-----',doctor_id)

    
#     return JsonResponse({'status':'admit'})


@login_required(login_url='/')
@csrf_exempt    
def Admit_patient_data(request):
    if request.method == "POST":
        discharge_id=request.POST['id']
        print('id-----------------',discharge_id)
        room_charge=request.POST['room_charge']
        print('r------------',room_charge)
        medicine_charges=request.POST['medicine_charge']
        print('m------------',medicine_charges)
        other_charges=request.POST['other_charges']
        print('o------------',other_charges)


        patient_Admitted_data=PatientAdmitted.objects.select_related('assignedDoctor').filter(id=discharge_id)
        for i in patient_Admitted_data:
            fees=i.assignedDoctor.fees
            # print('-------------',i.admitDate)
            # print('-------------',i.releaseDate)
            d=i.releaseDate-i.admitDate
        

            
        p1=PatientAdmitted.objects.filter(id=discharge_id).update(roomCharge=room_charge,medicineCost=medicine_charges,daySpent=d.days,doctorFee=fees,OtherCharge=other_charges,Staus_by_hospital=True)
        print('p1-------------------------',p1)


        return JsonResponse({'status':'charges_add'})
    
    admit_data=PatientAdmitted.objects.all()
    return render(request,'dashboard/hospital/admit_patient_data.html',context={'admit_Data':admit_data})





@login_required(login_url='/')      
@csrf_exempt
def Discharge_patient_dta(request):
    if request.method == "POST":
        discharge_id=request.POST['id']
        print(discharge_id)
        PatientAdmitted.objects.filter(id=discharge_id).update( is_discharged=True)
        
        return JsonResponse({'status':'discharge'})
    


    final_discharge_data=PatientAdmitted.objects.filter(Staus_by_hospital=True)
    l=[]
    for i in final_discharge_data:
        print('-------',i.patientId)
        hospital_check_payment_data=Payment.objects.filter(patient_data=i.id).order_by('-created_at').first()
        # for k in check_payment_data:
        #     print('---k--------------',k)

        l.append(hospital_check_payment_data)
       
    contxt=list(zip(final_discharge_data,l))
    print('c------',contxt)
    return render(request,'dashboard/hospital/discharge_patient_data.html',context={'final_discharge_data':contxt})

    
    
# for api 

from rest_framework import viewsets
from .serializer import User_Account_serializer,Patient_Profile_serializer,Doctor_Profile_serializer,Patient_Admitted_serializer,Payment_serializer,Appointment_serializer
from rest_framework.authentication import BasicAuthentication,SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django_filters import  rest_framework as filter
from rest_framework import filters



class show_user(viewsets.ModelViewSet):
    queryset=UserAccount.objects.all()
    serializer_class=User_Account_serializer
    # authentication_classes = [SessionAuthentication]
    # permission_classes = [IsAuthenticated]
    filter_backends=[filters.SearchFilter,]
    search_fields=['name']


class show_patient(viewsets.ModelViewSet):
    queryset=Patient_profile.objects.all()
    serializer_class=Patient_Profile_serializer


class show_doctor(viewsets.ModelViewSet):
    queryset=Doctor_profile.objects.all()
    serializer_class=Doctor_Profile_serializer


class show_Appointment(viewsets.ModelViewSet):
    queryset=Appointment.objects.all()
    serializer_class=Appointment_serializer


class show_patient_admitted(viewsets.ModelViewSet):
    queryset=PatientAdmitted.objects.all()
    serializer_class=Patient_Admitted_serializer


class show_payment(viewsets.ModelViewSet):
    queryset=Payment.objects.all()
    serializer_class=Payment_serializer