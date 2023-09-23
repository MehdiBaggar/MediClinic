# models.py
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class Doctor(AbstractUser):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    SPECIALITY_CHOICES = [
        ('gp', 'General Practitioner (GP)'),
        ('pediatrician', 'Pediatrician'),
        ('obgyn', 'Obstetrician/Gynecologist (OB/GYN)'),
        ('dermatologist', 'Dermatologist'),
        ('orthopedic_surgeon', 'Orthopedic Surgeon'),
        ('cardiologist', 'Cardiologist'),
        ('psychiatrist', 'Psychiatrist'),
    ]

    speciality = models.CharField(max_length=100, choices=SPECIALITY_CHOICES)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    bio = models.TextField(null=True,default='')
    phone = models.CharField(max_length=20,default='')
    date_of_birth = models.DateField(default='2001-04-20')
    hospital = models.TextField(null=True, default='MediClinic')
    experience = models.TextField(null=True,default='')
    working_hours = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='media/', blank=True, null=True)
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='doctor_set',  # Use a unique related_name
        related_query_name='user'
    )

    # Specify a unique related_name for user_permissions
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='doctor_set',  # Use a unique related_name
        related_query_name='user'
    )
