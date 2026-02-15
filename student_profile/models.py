from django.db import models
from django.contrib.auth.models import AbstractUser

class Student(AbstractUser):

    GENDER_CHOICES = [
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
        ("Prefer Not to Say", "Prefer Not to Say")
    ]
    PROGRAM_CHOICES = [
        ("Data Science", "Data Science"),
        ("Electronic Systems", "Electronic Systems"),
    ]
    LEVEL_CHOICES = [
        ("Foundation", "Foundation"),
        ("Diploma", "Diploma"),
        ("Degree", "Degree")
    ]

    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, null=True, blank=True)
    program = models.CharField(max_length=30, choices=PROGRAM_CHOICES, null=True, blank=True)
    level = models.CharField(max_length=30, choices=LEVEL_CHOICES, null=True, blank=True)
    profile_pic = models.URLField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    tagline = models.CharField(max_length=50, null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    is_core = models.BooleanField(default=False)
    is_uhc = models.BooleanField(default=False)

    def __str__(self):
        return self.username
