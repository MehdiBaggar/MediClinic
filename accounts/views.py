from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .forms import DoctorCreationForm
from .models import Doctor
from Medi.models import Patient
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from django.contrib.auth.decorators import login_required



@login_required
def doctor_home(request):
    patients = Patient.objects.all()[:5]
    user = request.user
    doctor_count = Doctor.objects.count()
    patient_count = Patient.objects.count()


    return render(request, 'doctor-home.html',{'patients':patients,'user' : user,'doctor_count':doctor_count,'patient_count':patient_count})


@login_required
def doctor_patient_list(request):
    patients = Patient.objects.all()
    user = request.user
    return render(request, 'doctor-patient-list.html', {'patients':patients,'user' : user})

@login_required
def doctor_prescriptions(request):
    patients = Patient.objects.all()
    user = request.user
    return render(request, 'doctor-prescription.html', {'patients':patients,'user' : user})


@login_required
def doctor_appointement(request):
    patient = Patient.objects.all()
    doctor = Doctor.objects.all()
    user = request.user
    return render(request, 'doctor-calendar.html', {'patient': patient, 'user': user, 'doctor': doctor})


def user_login(request):
    if request.method == 'POST':
        username_or_email = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username_or_email, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                if user.is_superuser:
                    return redirect('/Medi')  # Redirect superuser to admin page
                else:
                    messages.error(request, 'Your are doctor.')
            else:
                messages.error(request, 'Your account is inactive.')
        else:
            messages.error(request, 'Invalid login credentials.')

    return render(request, 'login.html',)

def doctor_login(request):
    if request.method == 'POST':
        username_or_email = request.POST['username']
        password = request.POST['password']

        doctor = authenticate(request, username=username_or_email, password=password)

        if doctor is not None:
            if doctor.is_active:
                login(request, doctor)
                return redirect('doctor-home',)  # Redirect doctors to the regular user home page
            else:
                messages.error(request, 'Your account is inactive.')
        else:
            messages.error(request, 'Invalid login credentials.')

    return render(request, 'doctor_login.html',)


def register_doctore(request):
    if request.method == 'POST':
        form = DoctorCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('doctor_login')  # Redirect to the doctor's dashboard
    else:
        form = DoctorCreationForm()
    return render(request, 'doctor_registration.html', {'form': form})

def home_page(request):
    return render(request, 'home-page.html',)

@login_required
def doctor_payment(request):
    patients = Patient.objects.all()
    user = request.user
    return render(request, 'doctor-payment.html', {'patients':patients, 'user' : user})