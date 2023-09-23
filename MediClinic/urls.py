"""
URL configuration for MediClinic project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from accounts import views
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Medi/', include('Medi.urls')),
    path("DoctorHome/", views.doctor_home, name='doctor-home'),
    path('Patiens-list', views.doctor_patient_list, name='doctor-patient-list'),
    path('DoctorPrescriptions', views.doctor_prescriptions, name='doctor-prescriptions'),
    path('Appointement', views.doctor_appointement, name='doctor-appointement'),
    path('Payment', views.doctor_payment, name='doctor-payment'),
    path('', lambda request: redirect('home') if request.user.is_authenticated and request.user.is_superuser else (redirect('doctor-home') if request.user.is_authenticated else redirect('home-page')),name='home_p'),
    path("Home/", views.home_page, name='home-page'),
    path("login/", views.user_login, name='login'),
    path("register/", views.register_doctore, name='register'),
    path('doctorlogin/', views.doctor_login, name='doctor_login'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


