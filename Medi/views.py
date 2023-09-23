from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Patient, Payment
from accounts.models import Doctor
from django.shortcuts import render, get_object_or_404
from reportlab.lib.pagesizes import letter
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from django.conf import settings
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta

@login_required
def index(request):
    patients = Patient.objects.all()[:5]
    user = request.user
    doctor_count = Doctor.objects.count()
    patient_count = Patient.objects.count()


    return render(request, 'index.html',{'patients':patients,'user' : user,'doctor_count':doctor_count,'patient_count':patient_count})



def new(request):
    return HttpResponse("new page")




@login_required
def user_profile(request):
    try:
        doctor = Doctor.objects.get(id=request.user.id)  # Get the logged-in doctor
    except Doctor.DoesNotExist:
        doctor = None

    if request.method == 'POST':
        # Get the form data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone_number')
        speciality = request.POST.get('speciality')
        gender = request.POST.get('gender')
        bio = request.POST.get('bio')

        if doctor:
            # Update the doctor's information in the database
            doctor.first_name = first_name
            doctor.last_name = last_name
            doctor.email = email
            doctor.phone = phone
            doctor.speciality = speciality
            doctor.gender = gender
            doctor.bio = bio

            # Save the changes
            doctor.save()

    return render(request, 'user-profile.html', {'doctor': doctor})


@login_required
def patient_list(request):
    patients = Patient.objects.all()
    user = request.user
    return render(request, 'patient-page.html', {'patients':patients,'user' : user})


@login_required
def doctor_list(request):
    doctor = Doctor.objects.all()
    user = request.user
    return render(request, 'doctors-page.html', {'doctor':doctor,'user' : user})


@login_required
def patient_full(request, patient_id):

    patient = get_object_or_404(Patient, pk=patient_id)
    if patient.doctor_id:
        doctor = get_object_or_404(Doctor, id=patient.doctor_id)
    else:
        doctor = None
    return render(request, 'patient-full.html',{'patient': patient, 'doctor': doctor})

@login_required
def doctor_full(request, doctor_id):

    doctor = get_object_or_404(Doctor, pk=doctor_id)
    current_year = datetime.now().year
    age = current_year - doctor.date_of_birth.year
    return render(request, 'doctor_full.html',{'doctor': doctor,'age':age})

@login_required
def edit_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    doctor = Doctor.objects.all()



    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        status = request.POST.get('status')
        blood_type = request.POST.get('blood_type')
        height = request.POST.get('height')
        weight = request.POST.get('weight')
        allergies = request.POST.get('allergies')
        diagnosis = request.POST.get('diagnosis')
        doctor_id = request.POST.get('doctor')
        date_of_birth = request.POST.get('date_of_birth')
        photo = request.FILES.get('photo')
        prescription = request.POST.get('prescription')
        medication = request.POST.get('medication')
        traitement = request.POST.get('traitement')




        if patient:
            # Update the doctor's information in the database
            patient.first_name = first_name
            patient.last_name = last_name
            patient.email = email
            patient.phone = phone
            patient.age = age
            patient.gender = gender
            patient.status = status
            patient.blood_type = blood_type
            patient.weight = weight
            patient.height = height
            patient.allergies = allergies
            patient.diagnosis = diagnosis
            patient.doctor_id = doctor_id
            patient.date_of_birth = date_of_birth
            patient.prescription = prescription
            patient.medication = medication
            patient.traitement = traitement
            if not photo:
                patient.photo = patient.photo
            else:
                patient.photo = photo

            # Save the changes
            patient.save()
            return redirect('patient-full', patient_id=patient_id)
    return render(request, 'edit_patient.html', {'patient': patient,'doctor':doctor})


@login_required
def edit_doctor(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)


    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender')
        date_of_birth = request.POST.get('date_of_birth')
        speciality = request.POST.get('speciality')
        experience = request.POST.get('experience')
        working_hours = request.POST.get('working_hours')
        hospital = request.POST.get('hospital')
        photo = request.FILES.get('photo')



        if doctor:
            # Update the doctor's information in the database
            doctor.first_name = first_name
            doctor.last_name = last_name
            doctor.email = email
            doctor.phone = phone
            doctor.gender = gender
            doctor.speciality = speciality
            doctor.date_of_birth = date_of_birth
            doctor.hospital = hospital
            doctor.working_hours = working_hours
            doctor.experience = experience


            if not photo:
                doctor.photo =doctor.photo
            else:
                doctor.photo = photo





            # Save the changes
            doctor.save()
            return redirect('doctor-full', doctor_id=doctor_id)
    return render(request, 'edit_doctor.html', {'doctor':doctor})


@login_required
def add_doctor(request,):
    doctor = Doctor.objects.all()
    default_image_path = settings.STATIC_URL + 'static/images/img.jpeg'


    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender')
        date_of_birth = request.POST.get('date_of_birth')
        speciality = request.POST.get('speciality')
        experience = request.POST.get('experience')
        working_hours = request.POST.get('working_hours')
        hospital = request.POST.get('hospital')
        photo = request.FILES.get('photo')



        doctor = Doctor(
            # Update the doctor's information in the database
            username=first_name + '_' +last_name,
            first_name = first_name,
            last_name = last_name,
            email = email,
            phone = phone,
            gender = gender,
            speciality = speciality,
            date_of_birth = date_of_birth,
            hospital = hospital,
            working_hours = working_hours,
            experience = experience,
            photo = photo,
            )

        if not photo:
                doctor.photo = default_image_path



        doctor.save()
        return redirect('doctor-list',)
    return render(request, 'add_doctor.html', {'doctor':doctor})


@login_required
def add_patient(request):

    doctor = Doctor.objects.all()
    default_image_path = settings.STATIC_URL + 'static/images/img.jpeg'

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        status = request.POST.get('status')
        blood_type = request.POST.get('blood_type')
        height = request.POST.get('height')
        weight = request.POST.get('weight')
        allergies = request.POST.get('allergies')
        diagnosis = request.POST.get('diagnosis')
        doctor_id = request.POST.get('doctor')
        date_of_birth = request.POST.get('date_of_birth')
        photo = request.FILES.get('photo')

        patient = Patient(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            age=age,
            gender=gender,
            status=status,
            blood_type=blood_type,
            weight=weight,
            height=height,
            allergies=allergies,
            diagnosis=diagnosis,
            doctor_id=doctor_id,
            date_of_birth=date_of_birth,
            photo=photo,


        )
        if not photo:
            patient.photo = default_image_path

        patient.save()
        return redirect('patient-list',)
    return render(request, 'add_patient.html', {'doctor':doctor})



@login_required
def prescriptions(request):
    patients = Patient.objects.all()
    user = request.user
    return render(request, 'prescriprtions.html', {'patients':patients,'user' : user})



@login_required
def payment(request):
    patients = Patient.objects.all()
    user = request.user
    return render(request, 'payment.html', {'patients':patients, 'user' : user})



@login_required
def delete_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    patient.delete()
    return redirect('patient-list')  # Redirect to patient list page after deletion



@login_required
def delete_doctor(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    doctor.delete()
    return redirect('doctor-list')  # Redirect to patient list page after deletion


@login_required
def appointement(request):
    patient = Patient.objects.all()
    doctor = Doctor.objects.all()
    user = request.user
    return render(request, 'calendar.html', {'patient': patient, 'user': user, 'doctor': doctor})



@login_required
def generate_pdf(request, patient_id, doctor_id):

    patient = get_object_or_404(Patient, id=patient_id)
    doctor = get_object_or_404(Doctor, id=doctor_id)

    # Create a BytesIO buffer to receive PDF content
    buffer = BytesIO()

    # Create the PDF object, using the BytesIO buffer as its "file"
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()

    # Define your styles for different elements
    normal_style = styles['Normal']
    heading_style = styles['Heading1']

    # Build the document content
    elements = []

    # Add Doctor's information
    elements.append(Paragraph(f"Doctor information:", heading_style))
    elements.append(Paragraph(f"{doctor.first_name} ", normal_style))
    elements.append(Paragraph(f"{doctor.last_name}", normal_style))
    elements.append(Paragraph(f"MEDICLINIC", normal_style))
    elements.append(Paragraph(f"Phone: {doctor.phone}", normal_style))
    elements.append(Paragraph(f"Email: {doctor.email}", normal_style))
    elements.append(Spacer(1, 12))  # Add some space

    # Add Patient's information
    elements.append(Paragraph("Patient Information:", heading_style))
    elements.append(Paragraph(f"Patient Name: {patient.first_name} {patient.last_name}", normal_style))
    elements.append(Paragraph(f"Date of Birth: {patient.date_of_birth}", normal_style))
    elements.append(Paragraph(f"Gender: {patient.gender}", normal_style))
    elements.append(Paragraph(f"Address: {patient.address}", normal_style))
    elements.append(Paragraph(f"Phone Number: {patient.phone}", normal_style))
    elements.append(Paragraph(f"Email Address: {patient.email}", normal_style))
    elements.append(Paragraph(f"diagnosis: {patient.diagnosis}", normal_style))
    elements.append(Spacer(1, 12))
    if patient.diagnosis == "Hypertension (High Blood Pressure)":
        elements.append(Paragraph("Prescription:", heading_style))
        elements.append(Paragraph("Medication: Lisinopril", normal_style))
        elements.append(Paragraph("Dosage: 10 mg", normal_style))
        elements.append(Paragraph("Route: Oral", normal_style))
        elements.append(Paragraph("Frequency: Take 10 mg once daily in the morning.", normal_style))
        elements.append(Paragraph("Duration: Ongoing", normal_style))
        elements.append(Paragraph("Refills: 3", normal_style))
        elements.append(Paragraph("Instructions to Patient:", heading_style))
        instructions = [
            "Take the medication with or without food.",
            "Monitor your blood pressure regularly.",
            "Contact our office if you experience any unusual symptoms.",
            "Attend a follow-up appointment in 4 weeks."
        ]
        for instruction in instructions:
            elements.append(Paragraph(f"- {instruction}", normal_style))
        elements.append(Paragraph(f"Signature: ________{doctor.last_name}_________", normal_style))
        elements.append(Paragraph(f"Dr. {doctor.last_name}", normal_style))
        elements.append(Paragraph("This prescription is valid until August 17, 2024.", normal_style))
    elif patient.diagnosis == "Type 2 Diabetes":
        elements.append(Paragraph("Prescription:", heading_style))
        elements.append(Paragraph("Medication: Insulin", normal_style))
        elements.append(Paragraph("Dosage: As prescribed", normal_style))
        elements.append(Paragraph("Route: Subcutaneous", normal_style))
        elements.append(Paragraph("Frequency: Follow your doctor's instructions.", normal_style))
        elements.append(Paragraph("Duration: Ongoing", normal_style))
        elements.append(Paragraph("Refills: As prescribed", normal_style))
        elements.append(Paragraph("Instructions to Patient:", heading_style))
        instructions = [
            "Administer insulin as directed by your doctor.",
            "Monitor your blood sugar levels regularly.",
            "Follow a healthy diet and exercise regimen.",
            "Contact our office if you experience any unusual symptoms.",
            "Attend regular check-ups."
        ]
        for instruction in instructions:
            elements.append(Paragraph(f"- {instruction}", normal_style))
        elements.append(Paragraph(f"Signature: ________{doctor.last_name}_________", normal_style))
        elements.append(Paragraph(f"Dr. {doctor.last_name}", normal_style))

        elements.append(Paragraph("This prescription is valid until August 17, 2024.", normal_style))
    elif patient.diagnosis == "Asthma":
            elements.append(Paragraph("Prescription:", heading_style))
            elements.append(Paragraph("Medication: Albuterol", normal_style))
            elements.append(Paragraph("Dosage: 2 puffs every 4-6 hours", normal_style))
            elements.append(Paragraph("Route: Inhalation", normal_style))
            elements.append(Paragraph("Frequency: Use as needed for breathing difficulties.", normal_style))
            elements.append(Paragraph("Duration: Ongoing", normal_style))
            elements.append(Paragraph("Refills: As needed", normal_style))
            elements.append(Paragraph("Instructions to Patient:", heading_style))
            instructions = [
                "Use the inhaler as directed to relieve asthma symptoms.",
                "Carry the inhaler with you at all times.",
                "Avoid triggers that worsen your asthma symptoms.",
                "Contact our office if you experience severe breathing difficulties or worsening symptoms.",
                "Attend regular check-ups."
            ]
            for instruction in instructions:
                elements.append(Paragraph(f"- {instruction}", normal_style))
            elements.append(Paragraph(f"Signature: ________{doctor.last_name}_________", normal_style))
            elements.append(Paragraph(f"Dr. {doctor.last_name}", normal_style))
            elements.append(Paragraph("This prescription is valid until August 17, 2024.", normal_style))
    elif patient.diagnosis == "Allergic Rhinitis":
        elements.append(Paragraph("Prescription:", heading_style))
        elements.append(Paragraph("Medication: Loratadine", normal_style))
        elements.append(Paragraph("Dosage: 10 mg once daily", normal_style))
        elements.append(Paragraph("Route: Oral", normal_style))
        elements.append(Paragraph("Frequency: Take 10 mg once daily.", normal_style))
        elements.append(Paragraph("Duration: As needed", normal_style))
        elements.append(Paragraph("Refills: As needed", normal_style))
        elements.append(Paragraph("Instructions to Patient:", heading_style))
        instructions = [
            "Take the medication with or without food.",
            "Avoid allergens that trigger your symptoms.",
            "Contact our office if your symptoms worsen or if you experience any adverse effects.",
            "Attend regular check-ups."
        ]
        for instruction in instructions:
            elements.append(Paragraph(f"- {instruction}", normal_style))
        elements.append(Paragraph(f"Signature: ________{doctor.last_name}_________", normal_style))
        elements.append(Paragraph(f"Dr. {doctor.last_name}", normal_style))
        elements.append(Paragraph("This prescription is valid until August 17, 2024.", normal_style))
    
    elif patient.diagnosis == "Migraine":
        elements.append(Paragraph("Prescription:", heading_style))
        elements.append(Paragraph("Medication: Sumatriptan", normal_style))
        elements.append(Paragraph("Dosage: 50 mg at onset of migraine", normal_style))
        elements.append(Paragraph("Route: Oral", normal_style))
        elements.append(Paragraph("Frequency: Take 50 mg at the onset of a migraine attack.", normal_style))
        elements.append(Paragraph("Duration: As needed", normal_style))
        elements.append(Paragraph("Refills: As needed", normal_style))
        elements.append(Paragraph("Instructions to Patient:", heading_style))
        instructions = [
            "Take the medication at the first sign of a migraine attack.",
            "Avoid triggers that worsen your migraines.",
            "Contact our office if your migraines become more frequent or severe.",
            "Attend regular check-ups."
        ]
        for instruction in instructions:
            elements.append(Paragraph(f"- {instruction}", normal_style))
        elements.append(Paragraph(f"Signature: ________{doctor.last_name}_________", normal_style))
        elements.append(Paragraph(f"Dr. {doctor.last_name}", normal_style))
        elements.append(Paragraph("This prescription is valid until August 17, 2024.", normal_style))
    elif patient.diagnosis == "Depression":
        elements.append(Paragraph("Prescription:", heading_style))
        elements.append(Paragraph("Medication: Sertraline", normal_style))
        elements.append(Paragraph("Dosage: 50 mg", normal_style))
        elements.append(Paragraph("Route: Oral", normal_style))
        elements.append(Paragraph("Frequency: Take 50 mg once daily.", normal_style))
        elements.append(Paragraph("Duration: Ongoing", normal_style))
        elements.append(Paragraph("Refills: 3", normal_style))
        elements.append(Paragraph("Instructions to Patient:", heading_style))
        instructions = [
            "Take the medication with or without food.",
            "Attend therapy sessions as scheduled.",
            "Contact our office if you experience any worsening of symptoms or side effects.",
            "Attend regular check-ups."
        ]
        for instruction in instructions:
            elements.append(Paragraph(f"- {instruction}", normal_style))
        elements.append(Paragraph(f"Signature: ________{doctor.last_name}_________", normal_style))
        elements.append(Paragraph(f"Dr. {doctor.last_name}", normal_style))
        elements.append(Paragraph("This prescription is valid until August 17, 2024.", normal_style))
    elif patient.diagnosis == "Anxiety Disorder":
        elements.append(Paragraph("Prescription:", heading_style))
        elements.append(Paragraph("Medication: Alprazolam", normal_style))
        elements.append(Paragraph("Dosage: 0.5 mg", normal_style))
        elements.append(Paragraph("Route: Oral", normal_style))
        elements.append(Paragraph("Frequency: Take 0.5 mg twice daily as needed.", normal_style))
        elements.append(Paragraph("Duration: As needed", normal_style))
        elements.append(Paragraph("Refills: 0", normal_style))
        elements.append(Paragraph("Instructions to Patient:", heading_style))
        instructions = [
            "Take the medication as needed for anxiety symptoms.",
            "Avoid alcohol while taking this medication.",
            "Contact our office if you experience any unusual side effects.",
            "Attend therapy sessions as scheduled."
        ]
        for instruction in instructions:
            elements.append(Paragraph(f"- {instruction}", normal_style))
        elements.append(Paragraph(f"Signature: ________{doctor.last_name}_________", normal_style))
        elements.append(Paragraph(f"Dr. {doctor.last_name}", normal_style))
        elements.append(Paragraph("This prescription is valid until August 17, 2024.", normal_style))
    elif patient.diagnosis == "Obesity":
        elements.append(Paragraph("Prescription:", heading_style))
        elements.append(Paragraph("Recommendation: Weight Management Plan", normal_style))
        elements.append(Paragraph("Dietary Guidelines:", heading_style))
        diet_guidelines = [
            "Consume a balanced diet rich in vegetables, fruits, whole grains, lean proteins, and healthy fats.",
            "Limit intake of sugary beverages, processed foods, and high-calorie snacks.",
            "Control portion sizes to avoid overeating.",
            "Stay hydrated by drinking plenty of water throughout the day.",
            "Consider consulting a registered dietitian for personalized meal planning."
        ]
        for guideline in diet_guidelines:
            elements.append(Paragraph(f"- {guideline}", normal_style))
        elements.append(Paragraph("Physical Activity Recommendations:", heading_style))
        physical_activity = [
            "Engage in at least 150 minutes of moderate-intensity aerobic activity or 75 minutes of vigorous-intensity aerobic activity per week.",
            "Incorporate strength training exercises for all major muscle groups at least two days a week.",
            "Find enjoyable physical activities such as walking, swimming, cycling, or dancing.",
            "Gradually increase activity levels and set achievable goals."
        ]
        for activity in physical_activity:
            elements.append(Paragraph(f"- {activity}", normal_style))
        elements.append(Paragraph("Behavioral Changes:", heading_style))
        behavior_changes = [
            "Practice mindful eating by paying attention to hunger and fullness cues.",
            "Keep a food diary to track eating patterns and identify triggers for overeating.",
            "Get adequate sleep to support weight management and overall health.",
            "Seek support from healthcare professionals, support groups, or counseling if needed."
        ]
        for change in behavior_changes:
            elements.append(Paragraph(f"- {change}", normal_style))
        elements.append(Paragraph(f"Signature: ________{doctor.last_name}_________", normal_style))
        elements.append(Paragraph(f"Dr. {doctor.last_name}", normal_style))
    elif patient.diagnosis == "Chronic Obstructive Pulmonary Disease (COPD)":
        elements.append(Paragraph("Prescription:", heading_style))
        elements.append(Paragraph("Medication: Tiotropium", normal_style))
        elements.append(Paragraph("Dosage: 18 mcg", normal_style))
        elements.append(Paragraph("Route: Inhalation", normal_style))
        elements.append(Paragraph("Frequency: Take 1 inhalation (18 mcg) once daily.", normal_style))
        elements.append(Paragraph("Duration: Ongoing", normal_style))
        elements.append(Paragraph("Refills: 1", normal_style))
        elements.append(Paragraph("Instructions to Patient:", heading_style))
        instructions = [
            "Inhale the medication at the same time every day.",
            "Use a spacer if prescribed by your doctor.",
            "Rinse your mouth with water after using the inhaler.",
            "Keep track of your symptoms and report any changes to your doctor.",
            "Attend follow-up appointments as scheduled."
        ]
        for instruction in instructions:
            elements.append(Paragraph(f"- {instruction}", normal_style))
        elements.append(Paragraph(f"Signature: ________{doctor.last_name}_________", normal_style))
        elements.append(Paragraph(f"Dr. {doctor.last_name}", normal_style))
        elements.append(Paragraph("This prescription is valid until August 17, 2024.", normal_style))
    elif patient.diagnosis == "Coronary Artery Disease":
        elements.append(Paragraph("Prescription:", heading_style))
        elements.append(Paragraph("Medication: Aspirin", normal_style))
        elements.append(Paragraph("Dosage: 81 mg", normal_style))
        elements.append(Paragraph("Route: Oral", normal_style))
        elements.append(Paragraph("Frequency: Take 81 mg once daily.", normal_style))
        elements.append(Paragraph("Duration: Ongoing", normal_style))
        elements.append(Paragraph("Refills: 3", normal_style))
        elements.append(Paragraph("Instructions to Patient:", heading_style))
        instructions = [
            "Take the medication with or without food.",
            "Do not crush or chew the tablet.",
            "Contact our office if you experience any unusual bleeding or bruising.",
            "Attend follow-up appointments as scheduled."
        ]
        for instruction in instructions:
            elements.append(Paragraph(f"- {instruction}", normal_style))
        elements.append(Paragraph(f"Signature: ________{doctor.last_name}_________", normal_style))
        elements.append(Paragraph(f"Dr. {doctor.last_name}", normal_style))
        elements.append(Paragraph("This prescription is valid until August 17, 2024.", normal_style))
    elif patient.diagnosis == "Hyperthyroidism":
        elements.append(Paragraph("Prescription:", heading_style))
        elements.append(Paragraph("Medication: Methimazole", normal_style))
        elements.append(Paragraph("Dosage: 5 mg", normal_style))
        elements.append(Paragraph("Route: Oral", normal_style))
        elements.append(Paragraph("Frequency: Take 5 mg once daily.", normal_style))
        elements.append(Paragraph("Duration: Ongoing", normal_style))
        elements.append(Paragraph("Refills: 3", normal_style))
        elements.append(Paragraph("Instructions to Patient:", heading_style))
        instructions = [
            "Take the medication with or without food.",
            "Avoid excessive exposure to sunlight.",
            "Contact our office if you experience any unusual symptoms or side effects.",
            "Attend follow-up appointments as scheduled."
        ]
        for instruction in instructions:
            elements.append(Paragraph(f"- {instruction}", normal_style))
        elements.append(Paragraph(f"Signature: ________{doctor.last_name}_________", normal_style))
        elements.append(Paragraph(f"Dr. {doctor.last_name}", normal_style))
        elements.append(Paragraph("This prescription is valid until August 17, 2024.", normal_style))
    elif patient.diagnosis == "Hypothyroidism":
        elements.append(Paragraph("Prescription:", heading_style))
        elements.append(Paragraph("Medication: Levothyroxine", normal_style))
        elements.append(Paragraph("Dosage: 50 mcg", normal_style))
        elements.append(Paragraph("Route: Oral", normal_style))
        elements.append(Paragraph("Frequency: Take 50 mcg once daily on an empty stomach.", normal_style))
        elements.append(Paragraph("Duration: Ongoing", normal_style))
        elements.append(Paragraph("Refills: 3", normal_style))
        elements.append(Paragraph("Instructions to Patient:", heading_style))
        instructions = [
            "Take the medication at least 30 minutes before breakfast.",
            "Do not take other medications within 4 hours of levothyroxine.",
            "Contact our office if you experience any unusual symptoms or side effects.",
            "Attend follow-up appointments as scheduled."
        ]
        for instruction in instructions:
            elements.append(Paragraph(f"- {instruction}", normal_style))
        elements.append(Paragraph(f"Signature: ________{doctor.last_name}_________", normal_style))
        elements.append(Paragraph(f"Dr. {doctor.last_name}", normal_style))
        elements.append(Paragraph("This prescription is valid until August 17, 2024.", normal_style))
    elif patient.diagnosis == "Gastroesophageal Reflux Disease (GERD)":
        elements.append(Paragraph("Prescription:", heading_style))
        elements.append(Paragraph("Medication: Omeprazole", normal_style))
        elements.append(Paragraph("Dosage: 20 mg", normal_style))
        elements.append(Paragraph("Route: Oral", normal_style))
        elements.append(Paragraph("Frequency: Take 20 mg once daily before breakfast.", normal_style))
        elements.append(Paragraph("Duration: Ongoing", normal_style))
        elements.append(Paragraph("Refills: 3", normal_style))
        elements.append(Paragraph("Instructions to Patient:", heading_style))
        instructions = [
            "Take the medication before breakfast.",
            "Avoid lying down right after eating.",
            "Limit caffeine and spicy foods.",
            "Contact our office if you experience persistent symptoms."
        ]
        for instruction in instructions:
            elements.append(Paragraph(f"- {instruction}", normal_style))
        elements.append(Paragraph(f"Signature: ________{doctor.last_name}_________", normal_style))
        elements.append(Paragraph(f"Dr. {doctor.last_name}", normal_style))
        elements.append(Paragraph("This prescription is valid until August 17, 2024.", normal_style))
    elif patient.diagnosis == "Rheumatoid Arthritis":
        elements.append(Paragraph("Prescription:", heading_style))
        elements.append(Paragraph("Medication: Methotrexate", normal_style))
        elements.append(Paragraph("Dosage: 10 mg", normal_style))
        elements.append(Paragraph("Route: Oral", normal_style))
        elements.append(Paragraph("Frequency: Take 10 mg once weekly.", normal_style))
        elements.append(Paragraph("Duration: Ongoing", normal_style))
        elements.append(Paragraph("Refills: 3", normal_style))
        elements.append(Paragraph("Instructions to Patient:", heading_style))
        instructions = [
            "Take the medication on the same day each week.",
            "Monitor for any signs of infection.",
            "Follow up with your rheumatologist regularly.",
            "Contact our office if you experience any unusual side effects."
        ]
        for instruction in instructions:
            elements.append(Paragraph(f"- {instruction}", normal_style))
        elements.append(Paragraph(f"Signature: ________{doctor.last_name}_________", normal_style))
        elements.append(Paragraph(f"Dr. {doctor.last_name}", normal_style))
        elements.append(Paragraph("This prescription is valid until August 17, 2024.", normal_style))
    elif patient.diagnosis == "Osteoarthritis":
        elements.append(Paragraph("Prescription:", heading_style))
        elements.append(Paragraph("Medication: Acetaminophen", normal_style))
        elements.append(Paragraph("Dosage: 500 mg", normal_style))
        elements.append(Paragraph("Route: Oral", normal_style))
        elements.append(Paragraph("Frequency: Take 500 mg every 6 hours as needed for pain.", normal_style))
        elements.append(Paragraph("Duration: As needed", normal_style))
        elements.append(Paragraph("Refills: 0", normal_style))
        elements.append(Paragraph("Instructions to Patient:", heading_style))
        instructions = [
            "Take the medication as needed for pain.",
            "Avoid exceeding the recommended dose.",
            "Follow up with your healthcare provider if pain persists.",
            "Engage in gentle exercise and physical therapy as advised."
        ]
        for instruction in instructions:
            elements.append(Paragraph(f"- {instruction}", normal_style))
        elements.append(Paragraph(f"Signature: ________{doctor.last_name}_________", normal_style))
        elements.append(Paragraph(f"Dr. {doctor.last_name}", normal_style))
        elements.append(Paragraph("This prescription is valid until August 17, 2024.", normal_style))
    elif patient.diagnosis == "Eczema":
        elements.append(Paragraph("Prescription:", heading_style))
        elements.append(Paragraph("Medication: Hydrocortisone Cream", normal_style))
        elements.append(Paragraph("Dosage: Apply a thin layer to affected areas", normal_style))
        elements.append(Paragraph("Route: Topical", normal_style))
        elements.append(Paragraph("Frequency: Apply twice daily to affected skin.", normal_style))
        elements.append(Paragraph("Duration: 2 weeks", normal_style))
        elements.append(Paragraph("Refills: 0", normal_style))
        elements.append(Paragraph("Instructions to Patient:", heading_style))
        instructions = [
            "Wash and dry the affected area before applying the cream.",
            "Avoid applying to open wounds or broken skin.",
            "Avoid using the cream on your face unless directed by your healthcare provider.",
            "If symptoms worsen or persist, contact our office for a follow-up."
        ]
        for instruction in instructions:
            elements.append(Paragraph(f"- {instruction}", normal_style))
        elements.append(Paragraph(f"Signature: ________{doctor.last_name}_________", normal_style))
        elements.append(Paragraph(f"Dr. {doctor.last_name}", normal_style))
        elements.append(Paragraph("This prescription is valid until August 17, 2024.", normal_style))
    elif patient.diagnosis == "Psoriasis":
        elements.append(Paragraph("Prescription:", heading_style))
        elements.append(Paragraph("Medication: Calcipotriene Cream", normal_style))
        elements.append(Paragraph("Dosage: Apply a thin layer to affected areas", normal_style))
        elements.append(Paragraph("Route: Topical", normal_style))
        elements.append(Paragraph("Frequency: Apply once daily to affected skin.", normal_style))
        elements.append(Paragraph("Duration: 4 weeks", normal_style))
        elements.append(Paragraph("Refills: 1", normal_style))
        elements.append(Paragraph("Instructions to Patient:", heading_style))
        instructions = [
            "Wash and dry the affected area before applying the cream.",
            "Avoid applying to open wounds or broken skin.",
            "Avoid using the cream on your face unless directed by your healthcare provider.",
            "Limit sun exposure while using this medication."
        ]
        for instruction in instructions:
            elements.append(Paragraph(f"- {instruction}", normal_style))
        elements.append(Paragraph(f"Signature: ________{doctor.last_name}_________", normal_style))
        elements.append(Paragraph(f"Dr. {doctor.last_name}", normal_style))
        elements.append(Paragraph("This prescription is valid until August 17, 2024.", normal_style))
    elif patient.diagnosis == "Celiac Disease":
        elements.append(Paragraph("Prescription:", heading_style))
        elements.append(Paragraph("Medication: Gluten-Free Diet", normal_style))
        elements.append(Paragraph("Dosage: Avoid foods containing gluten", normal_style))
        elements.append(Paragraph("Route: Dietary", normal_style))
        elements.append(Paragraph("Frequency: Follow a gluten-free diet", normal_style))
        elements.append(Paragraph("Duration: Ongoing", normal_style))
        elements.append(Paragraph("Refills: N/A", normal_style))
        elements.append(Paragraph("Instructions to Patient:", heading_style))
        instructions = [
            "Strictly avoid foods containing gluten, such as wheat, barley, and rye.",
            "Read labels carefully to ensure gluten-free products.",
            "Consider working with a dietitian to plan meals.",
            "Contact our office if you experience any digestive symptoms or complications.",
            "Attend a follow-up appointment as scheduled.",
        ]
        for instruction in instructions:
            elements.append(Paragraph(f"- {instruction}", normal_style))
        elements.append(Paragraph(f"Signature: ________{doctor.last_name}_________", normal_style))
        elements.append(Paragraph(f"Dr. {doctor.last_name}", normal_style))
        elements.append(Paragraph("This prescription is valid until August 17, 2024.", normal_style))
    elif patient.diagnosis == "Irritable Bowel Syndrome (IBS)":
        elements.append(Paragraph("Prescription:", heading_style))
        elements.append(Paragraph("Medication: Peppermint Oil Capsules", normal_style))
        elements.append(Paragraph("Dosage: 0.2 ml (181 mg) per capsule", normal_style))
        elements.append(Paragraph("Route: Oral", normal_style))
        elements.append(Paragraph("Frequency: Take 1 capsule three times daily before meals.", normal_style))
        elements.append(Paragraph("Duration: As needed", normal_style))
        elements.append(Paragraph("Refills: 0", normal_style))
        elements.append(Paragraph("Instructions to Patient:", heading_style))
        instructions = [
            "Take the medication as needed for digestive symptoms.",
            "Swallow the capsule whole with water.",
            "Do not chew or break the capsule.",
            "Contact our office if you experience any side effects or worsening symptoms.",
            "Follow a balanced diet and stay hydrated.",
        ]
        for instruction in instructions:
            elements.append(Paragraph(f"- {instruction}", normal_style))
        elements.append(Paragraph(f"Signature: ________{doctor.last_name}_________", normal_style))
        elements.append(Paragraph(f"Dr. {doctor.last_name}", normal_style))
        elements.append(Paragraph("This prescription is valid until August 17, 2024.", normal_style))
    elif patient.diagnosis == "Chronic Kidney Disease":
        elements.append(Paragraph("Prescription:", heading_style))
        elements.append(Paragraph("Medication: Erythropoietin (EPO)", normal_style))
        elements.append(Paragraph("Dosage: As prescribed by the doctor", normal_style))
        elements.append(Paragraph("Route: Subcutaneous injection", normal_style))
        elements.append(Paragraph("Frequency: As prescribed by the doctor", normal_style))
        elements.append(Paragraph("Duration: Ongoing", normal_style))
        elements.append(Paragraph("Refills: 0", normal_style))
        elements.append(Paragraph("Instructions to Patient:", heading_style))
        instructions = [
            "Administer the injection exactly as prescribed by your doctor.",
            "Keep track of your appointments for dose adjustments.",
            "Report any unusual symptoms or side effects to your doctor.",
            "Follow a kidney-friendly diet and stay hydrated.",
        ]
        for instruction in instructions:
            elements.append(Paragraph(f"- {instruction}", normal_style))
        elements.append(Paragraph(f"Signature: ________{doctor.last_name}_________", normal_style))
        elements.append(Paragraph(f"Dr. {doctor.last_name}", normal_style))
        elements.append(Paragraph("This prescription is valid until August 17, 2024.", normal_style))
    elif patient.diagnosis == "Stroke":
        elements.append(Paragraph("Prescription:", heading_style))
        elements.append(Paragraph("Medication: Aspirin", normal_style))
        elements.append(Paragraph("Dosage: 81 mg", normal_style))
        elements.append(Paragraph("Route: Oral", normal_style))
        elements.append(Paragraph("Frequency: Take 81 mg once daily.", normal_style))
        elements.append(Paragraph("Duration: Ongoing", normal_style))
        elements.append(Paragraph("Refills: 3", normal_style))
        elements.append(Paragraph("Instructions to Patient:", heading_style))
        instructions = [
            "Take the medication with a glass of water.",
            "Continue to take this medication unless advised otherwise by your doctor.",
            "Monitor for any signs of bleeding or stomach discomfort.",
            "Contact our office if you experience any unusual symptoms.",
            "Attend a follow-up appointment in 6 weeks.",
        ]
        for instruction in instructions:
            elements.append(Paragraph(f"- {instruction}", normal_style))
        elements.append(Paragraph(f"Signature: ________{doctor.last_name}_________", normal_style))
        elements.append(Paragraph(f"Dr. {doctor.last_name}", normal_style))
        elements.append(Paragraph("This prescription is valid until August 17, 2024.", normal_style))
    elif patient.diagnosis == "Alzheimer's Disease":
        elements.append(Paragraph("Prescription:", heading_style))
        elements.append(Paragraph("Medication: Donepezil", normal_style))
        elements.append(Paragraph("Dosage: 5 mg", normal_style))
        elements.append(Paragraph("Route: Oral", normal_style))
        elements.append(Paragraph("Frequency: Take 5 mg once daily at bedtime.", normal_style))
        elements.append(Paragraph("Duration: Ongoing", normal_style))
        elements.append(Paragraph("Refills: 3", normal_style))
        elements.append(Paragraph("Instructions to Patient:", heading_style))
        instructions = [
            "Take the medication at bedtime to reduce side effects.",
            "Continue to take this medication as prescribed.",
            "Monitor for any changes in memory or cognitive function.",
            "Contact our office if you experience any unusual symptoms.",
            "Attend a follow-up appointment in 6 weeks.",
        ]
        for instruction in instructions:
            elements.append(Paragraph(f"- {instruction}", normal_style))
        elements.append(Paragraph(f"Signature: ________{doctor.last_name}_________", normal_style))
        elements.append(Paragraph(f"Dr. {doctor.last_name}", normal_style))
        elements.append(Paragraph("This prescription is valid until August 17, 2024.", normal_style))
    elif patient.diagnosis == "Multiple Sclerosis":
        elements.append(Paragraph("Prescription:", heading_style))
        elements.append(Paragraph("Medication: Interferon Beta-1a", normal_style))
        elements.append(Paragraph("Dosage: 44 mcg", normal_style))
        elements.append(Paragraph("Route: Subcutaneous Injection", normal_style))
        elements.append(Paragraph("Frequency: Inject 44 mcg three times a week.", normal_style))
        elements.append(Paragraph("Duration: Ongoing", normal_style))
        elements.append(Paragraph("Refills: 3", normal_style))
        elements.append(Paragraph("Instructions to Patient:", heading_style))
        instructions = [
            "Administer the injection as directed by your healthcare provider.",
            "Rotate injection sites and follow proper injection technique.",
            "Monitor for any signs of infection or injection site reactions.",
            "Contact our office if you experience any unusual symptoms.",
            "Attend a follow-up appointment in 4 weeks.",
        ]
        for instruction in instructions:
            elements.append(Paragraph(f"- {instruction}", normal_style))
        elements.append(Paragraph(f"Signature: ________{doctor.last_name}_________", normal_style))
        elements.append(Paragraph(f"Dr. {doctor.last_name}", normal_style))
        elements.append(Paragraph("This prescription is valid until August 17, 2024.", normal_style))
    
    elif patient.diagnosis == "HIV/AIDS":
        elements.append(Paragraph("Prescription:", heading_style))
        elements.append(Paragraph("Medication: Tenofovir/Emtricitabine", normal_style))
        elements.append(Paragraph("Dosage: 300 mg/200 mg", normal_style))
        elements.append(Paragraph("Route: Oral", normal_style))
        elements.append(Paragraph("Frequency: Take one tablet daily.", normal_style))
        elements.append(Paragraph("Duration: Ongoing", normal_style))
        elements.append(Paragraph("Refills: 3", normal_style))
        elements.append(Paragraph("Instructions to Patient:", heading_style))
        instructions = [
            "Take the medication as prescribed to manage your condition.",
            "Continue to take this medication unless advised otherwise by your doctor.",
            "Monitor for any signs of side effects or changes in health.",
            "Contact our office if you experience any unusual symptoms.",
            "Attend a follow-up appointment in 3 months.",
        ]
        for instruction in instructions:
            elements.append(Paragraph(f"- {instruction}", normal_style))
        elements.append(Paragraph(f"Signature: ________{doctor.last_name}_________", normal_style))
        elements.append(Paragraph(f"Dr. {doctor.last_name}", normal_style))
        elements.append(Paragraph("This prescription is valid until August 17, 2024.", normal_style))
    elif patient.diagnosis == "Cancer":
        elements.append(Paragraph("Prescription:", heading_style))
        elements.append(Paragraph("Medication: Chemotherapy Regimen", normal_style))
        elements.append(Paragraph("Dosage: Varies based on regimen", normal_style))
        elements.append(Paragraph("Route: Intravenous", normal_style))
        elements.append(Paragraph("Frequency: As prescribed by oncologist", normal_style))
        elements.append(Paragraph("Duration: Ongoing", normal_style))
        elements.append(Paragraph("Refills: N/A", normal_style))
        elements.append(Paragraph("Instructions to Patient:", heading_style))
        instructions = [
            "Follow the chemotherapy schedule provided by your oncologist.",
            "Expect possible side effects; consult your oncologist for guidance.",
            "Monitor for any signs of infection or severe side effects.",
            "Contact our office immediately if you experience severe symptoms.",
            "Attend all scheduled appointments with your oncology team.",
        ]
        for instruction in instructions:
            elements.append(Paragraph(f"- {instruction}", normal_style))
        elements.append(Paragraph(f"Signature: ________{doctor.last_name}_________", normal_style))
        elements.append(Paragraph(f"Dr. {doctor.last_name}", normal_style))
        elements.append(Paragraph("This prescription is valid until August 17, 2024.", normal_style))

    # Build the PDF document
    doc.build(elements)

    # Get the value of the BytesIO buffer and create the response
    pdf = buffer.getvalue()
    buffer.close()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="patient_prescription.pdf"'
    response.write(pdf)
    return response

@login_required
def generate_bill_pdf(request, patient_id, doctor_id):
    # Retrieve patient and doctor objects
    patient = get_object_or_404(Patient, id=patient_id)
    doctor = get_object_or_404(Doctor, id=doctor_id)

    # Check if a Payment object exists for the patient
    payment, created = Payment.objects.get_or_create(patient=patient)


    # Update the fees based on diagnosis
    payment.update_fees()

    # Manually save the Payment object with updated fees
    payment.save()

    # Create a BytesIO buffer to receive PDF content
    buffer = BytesIO()

    # Create the PDF object, using the BytesIO buffer as its "file"
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()

    # Define your styles for different elements
    normal_style = styles['Normal']
    heading_style = styles['Heading1']

    # Build the document content
    elements = []

    # Add Doctor's information
    elements.append(Paragraph(f"Doctor Information:", heading_style))
    elements.append(Paragraph(f"Name: {doctor.first_name} {doctor.last_name}", normal_style))
    elements.append(Paragraph(f"Clinic: MEDICLINIC", normal_style))
    elements.append(Paragraph(f"Phone: {doctor.phone}", normal_style))
    elements.append(Paragraph(f"Email: {doctor.email}", normal_style))
    elements.append(Spacer(1, 12))  # Add some space

    # Add Patient's information
    elements.append(Paragraph("Patient Information:", heading_style))
    elements.append(Paragraph(f"Name: {patient.first_name} {patient.last_name}", normal_style))
    elements.append(Paragraph(f"Date of Birth: {patient.date_of_birth}", normal_style))
    elements.append(Paragraph(f"Gender: {patient.gender}", normal_style))
    elements.append(Paragraph(f"Address: {patient.address}", normal_style))
    elements.append(Paragraph(f"Phone Number: {patient.phone}", normal_style))
    elements.append(Paragraph(f"Email Address: {patient.email}", normal_style))
    elements.append(Spacer(1, 12))  # Add some space

    # Add Diagnosis Information
    elements.append(Paragraph("Diagnosis Information:", heading_style))
    elements.append(Paragraph(f"Diagnosis: {patient.diagnosis}", normal_style))
    elements.append(Spacer(1, 12))  # Add some space

    # Add Bill Information (You can customize this as needed)
    elements.append(Paragraph("Bill Information:", heading_style))
    elements.append(Paragraph(f"Consultation Fee: {payment.consultation_fee} MAD", normal_style))
    elements.append(Paragraph(f"Treatment Fee: {payment.treatment_fee} MAD", normal_style))
    elements.append(Paragraph(f"Medication Fee:{payment.medication_fee} MAD", normal_style))
    elements.append(Paragraph(f"Total Amount: {payment.total_fee} MAD", normal_style))

    # Build the PDF document
    doc.build(elements)

    # Rewind the buffer and create a response
    pdf = buffer.getvalue()
    buffer.close()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="patient_prescription.pdf"'
    response.write(pdf)
    return response