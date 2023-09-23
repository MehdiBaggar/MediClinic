from django.db import models
from accounts.models import Doctor
from django.contrib.auth.models import AbstractUser, Group, Permission


class Patient(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('stable', 'Stable'),
        ('improving', 'Improving'),
        ('critical', 'Critical'),
    ]

    BLOOD_TYPE_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]
    ALLERGIES_CHOICES = [
        ('Pollen', 'Pollen'),
        ('Dust Mites', 'Dust Mites'),
        ('Pet Dander', 'Pet Dander'),
        ('Mold', 'Mold'),
        ('Food Allergies', 'Food Allergies'),
        ('Insect Sting Allergies', 'Insect Sting Allergies'),
        ('Medication Allergies', 'Medication Allergies'),
        ('Latex Allergy', 'Latex Allergy'),
        ('Cockroach Allergy', 'Cockroach Allergy'),
        ('Other', 'Other'),
    ]
    DIAGNOSIS_CHOICES = [
        ('Hypertension (High Blood Pressure)', 'Hypertension (High Blood Pressure)'),
        ('Type 2 Diabetes', 'Type 2 Diabetes'),
        ('Asthma', 'Asthma'),
        ('Allergic Rhinitis', 'Allergic Rhinitis'),
        ('Migraine', 'Migraine'),
        ('Depression', 'Depression'),
        ('Anxiety Disorder', 'Anxiety Disorder'),
        ('Obesity', 'Obesity'),
        ('Chronic Obstructive Pulmonary Disease (COPD)', 'Chronic Obstructive Pulmonary Disease (COPD)'),
        ('Coronary Artery Disease', 'Coronary Artery Disease'),
        ('Hyperthyroidism', 'Hyperthyroidism'),
        ('Hypothyroidism', 'Hypothyroidism'),
        ('Gastroesophageal Reflux Disease (GERD)', 'Gastroesophageal Reflux Disease (GERD)'),
        ('Rheumatoid Arthritis', 'Rheumatoid Arthritis'),
        ('Osteoarthritis', 'Osteoarthritis'),
        ('Eczema', 'Eczema'),
        ('Psoriasis', 'Psoriasis'),
        ('Celiac Disease', 'Celiac Disease'),
        ('Irritable Bowel Syndrome (IBS)', 'Irritable Bowel Syndrome (IBS)'),
        ('Chronic Kidney Disease', 'Chronic Kidney Disease'),
        ('Stroke', 'Stroke'),
        ('Alzheimer\'s Disease', 'Alzheimer\'s Disease'),
        ('Multiple Sclerosis', 'Multiple Sclerosis'),
        ('HIV/AIDS', 'HIV/AIDS'),
        ('Cancer', 'Cancer'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Male')
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    photo = models.ImageField(upload_to='media/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    blood_type = models.CharField(max_length=5, choices=BLOOD_TYPE_CHOICES, default='A+')
    height = models.PositiveIntegerField(default=170)
    weight = models.PositiveIntegerField(default=100)
    allergies = models.CharField(max_length=50, choices=ALLERGIES_CHOICES, default='Other')
    diagnosis = models.CharField(max_length=100, choices=DIAGNOSIS_CHOICES, default='Hypertension')
    doctor_id = models.PositiveIntegerField(default=1)
    address = models.CharField(max_length=200)
    date_of_birth = models.DateField(default='2001-04-20')
    prescription = models.TextField(blank=True, null=True, default='')
    traitement = models.TextField(blank=True, null=True, default='')
    medication = models.TextField(blank=True, null=True, default='')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Payment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

    # Fields for consultation, treatment, medication, and total fees
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    treatment_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    medication_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def update_fees(self):
        # Calculate fees based on diagnosis and set total fee
        # You should implement the logic here to calculate the fees based on diagnosis
        # For example:
        if "Hypertension (High Blood Pressure)" in self.patient.diagnosis:
            self.consultation_fee = 250.00
            self.treatment_fee = 400.00
            self.medication_fee = 80.00
        elif "Type 2 Diabetes" in self.patient.diagnosis:
            self.consultation_fee = 250.00
            self.treatment_fee = 200.00
            self.medication_fee = 90.00
        elif "Asthma" in self.patient.diagnosis:
            self.consultation_fee = 250.00
            self.treatment_fee = 1600.00
            self.medication_fee = 250.00

        elif "Allergic Rhinitis" in self.patient.diagnosis:
            self.consultation_fee = 250.00
            self.treatment_fee = 1000.00
            self.medication_fee = 315.00

        elif "Migraine" in self.patient.diagnosis:
            self.consultation_fee = 250.00
            self.treatment_fee = 250.00
            self.medication_fee = 78.00

        elif "Depression" in self.patient.diagnosis:
            self.consultation_fee = 500.00
            self.treatment_fee = 650.00
            self.medication_fee = 300.00

        elif "Anxiety Disorder" in self.patient.diagnosis:
            self.consultation_fee = 250.00
            self.treatment_fee = 180.00
            self.medication_fee = 85.00

        elif "Obesity" in self.patient.diagnosis:
            self.consultation_fee = 350.00
            self.treatment_fee = 3000.00
            self.medication_fee = 515.00

        elif "Chronic Obstructive Pulmonary Disease (COPD)" in self.patient.diagnosis:
            self.consultation_fee = 350.00
            self.treatment_fee = 4000.00
            self.medication_fee = 1000.00
        elif "Coronary Artery Disease" in self.patient.diagnosis:
            self.consultation_fee = 350.00
            self.treatment_fee = 20000.00
            self.medication_fee = 2500.00
        elif "Hyperthyroidism" in self.patient.diagnosis:
            self.consultation_fee = 350.00
            self.treatment_fee = 450.00
            self.medication_fee = 150.00
        elif "Hypothyroidism" in self.patient.diagnosis:
            self.consultation_fee = 350.00
            self.treatment_fee = 400.00
            self.medication_fee = 150.00
        elif "Gastroesophageal Reflux Disease (GERD)" in self.patient.diagnosis:
            self.consultation_fee = 350.00
            self.treatment_fee = 12000.00
            self.medication_fee = 895.00
        elif "Rheumatoid Arthritis" in self.patient.diagnosis:
            self.consultation_fee = 350.00
            self.treatment_fee = 2000.00
            self.medication_fee = 450.00
        elif "Osteoarthritis" in self.patient.diagnosis:
            self.consultation_fee = 350.00
            self.treatment_fee = 1700.00
            self.medication_fee = 715.00
        elif "Eczema" in self.patient.diagnosis:
            self.consultation_fee = 350.00
            self.treatment_fee = 600.00
            self.medication_fee = 415.00
        elif "Psoriasis" in self.patient.diagnosis:
            self.consultation_fee = 350.00
            self.treatment_fee = 990.00
            self.medication_fee = 350.00
        elif "Celiac Disease" in self.patient.diagnosis:
            self.consultation_fee = 350.00
            self.treatment_fee = 90.00
            self.medication_fee = 15.00
        elif "Irritable Bowel Syndrome (IBS)" in self.patient.diagnosis:
            self.consultation_fee = 350.00
            self.treatment_fee = 7000.00
            self.medication_fee = 565.00

        elif "Chronic Kidney Disease" in self.patient.diagnosis:
            self.consultation_fee = 350.00
            self.treatment_fee = 3000.00
            self.medication_fee = 250.00
        elif "Stroke" in self.patient.diagnosis:
            self.consultation_fee = 350.00
            self.treatment_fee = 50000.00
            self.medication_fee = 1500.00
        elif "Alzheimer\'s Disease" in self.patient.diagnosis:
            self.consultation_fee = 350.00
            self.treatment_fee = 20000.00
            self.medication_fee = 115.00
        elif "Multiple Sclerosis" in self.patient.diagnosis:
            self.consultation_fee = 350.00
            self.treatment_fee = 4000.00
            self.medication_fee = 650.00
        elif "HIV/AIDS" in self.patient.diagnosis:
            self.consultation_fee = 350.00
            self.treatment_fee = 1800.00
            self.medication_fee = 3000.00
        elif "Cancer" in self.patient.diagnosis:
            self.consultation_fee = 350.00
            self.treatment_fee = 130000.00
            self.medication_fee = 999.00



        # Calculate total fee as the sum of all fees
        self.total_fee = (
                self.consultation_fee + self.treatment_fee + self.medication_fee
        )


