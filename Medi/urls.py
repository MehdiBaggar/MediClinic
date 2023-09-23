from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index, name='home'),
    path('new', views.new),
    path('UserProfile', views.user_profile, name='Userprofile'),
    path('Patiens-list', views.patient_list, name='patient-list'),
    path('patiens-list/<int:patient_id>/', views.patient_full, name='patient-full'),
    path('patiens-list/edit/<int:patient_id>/', views.edit_patient, name='edit_patient'),
    path('Prescriptions', views.prescriptions, name='prescriptions'),
    path('Prescriptions/<int:patient_id>/<int:doctor_id>/', views.generate_pdf, name='prescription-pdf'),
    path('patient/<int:patient_id>/delete/', views.delete_patient, name='delete_patient'),
    path('add_patient/', views.add_patient, name='add_patient'),
    path('add_doctor/', views.add_doctor, name='add_doctor'),
    path('Doctors-list/', views.doctor_list, name='doctor-list'),
    path('Doctors-list/<int:doctor_id>/', views.doctor_full, name='doctor-full'),
    path('Doctors-list/edit/<int:doctor_id>/', views.edit_doctor, name='edit_doctor'),
    path('Doctors-list/<int:doctor_id>/delete/', views.delete_doctor, name='delete_doctor'),
    path('Appointement', views.appointement, name='appointement'),
    path('Payment', views.payment, name='payment'),
    path('Payment/<int:patient_id>/<int:doctor_id>/', views.generate_bill_pdf, name='payment-pdf'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home-page'), name='logout'),
]



