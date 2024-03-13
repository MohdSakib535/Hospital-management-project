"""Hospital_Management_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from Doctor import views
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.routers import DefaultRouter
router=DefaultRouter()
router.register('userdata',views.show_user)
router.register('patientdata',views.show_patient)
router.register('doctordata',views.show_doctor)
router.register('appointmentdata',views.show_Appointment)
router.register('admitteddata',views.show_patient_admitted)
router.register('paymentdata',views.show_payment)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('about/',views.about,name='about'),
    path('Registraton',views.Registraton,name='registration'),
    path('token-send',views.Token_Send,name='token_send'),
    path('profile/',views.Profile,name='profile'),
    path('verify-token/<auth_token>',views.Verify_token,name='verify_token'),
    path('forget-password',views.Forget_password,name='forget_password'),
    path('change-password/<auth_token>/',views.Change_password,name='change_password'),


    path('login',views.Login,name='login'),
    # path('doctor-login',views.Doctor_login,name='doctor_login'),
    path('logout',views.Doctor_logout,name='logout'),
    # path('Patient-login',views.Patient_login,name='patient_login'),
    path('tables',views.tables,name='tables'),
    path('Dashboard',views.Dashboard,name='dashboard'),
    path('Doctor-data/',views.New_Doctor_Data,name='new_doctor_data'),
    path('Approved-Doctor-data',views.Approved_Doctor_Data,name='approved_doctor_data'),
    path('patient-data/',views.Patient_Data,name='patient_data'),
    path('search-doctor/',views.Search_Doctor,name='search_doctor'),
    path('search-doctor-name/',views.Search_Doctor_name,name='search_doctor_name'),
    path('filter-doctor-query/',views.Filtered_doctor_data,name='filter_doctor_query'),
    path('doctor-response-data/',views.Doctor_Response_Data,name='doctor_response_data'),

    path('appointment/',views.Appointment_Data,name='appointment_data'),
    path('doctor-appointment/',views.Doctor_Appointment,name='doctor_appointment_data'),
    path('appointment-delete/',views.Appointment_Delete,name='appointment_delete'),
    path('doctor-votes/',views.Doctor_votes,name='doctor_votes'),
    path('my-doctor/',views.Favourite_Doctor_Data,name='my_doctor'),
    path('admit-patient/',views.Admitted_Data_List,name='admitted_data_list'),
    path('payments/',views.Payments_data,name='payment'),
    # path('payment-success/<str:payment_id>/<str:order_id>/<str:signature>/',views.Payment_success,name='payment_success'),
    path('payment-success/',views.Payment_success,name='payment_success'),
    path('payments/invoice/<int:id>/',views.Invoice_Data,name='invoice_data'),
    path('invoice-data-download/<int:id>/',views.Invoice_Data_Download,name='invoice_data_download'),
    # for hospital
    path('admit-patient_data/',views.Admit_patient_data,name='admit_patient_data'),
    path('discharge-patient_dta/',views.Discharge_patient_dta,name='discharge_patient_dta'),


    #api data
    path('api/',include(router.urls)),





    path('__debug__/', include('debug_toolbar.urls')),

    

    



]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

