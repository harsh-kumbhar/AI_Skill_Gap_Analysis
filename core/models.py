from django.db import models
from django.contrib.auth.models import User
from datetime import date

# Extend user profile later for extra fields
class Profile(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )

    SALARY_CHOICES = (
        ('<3L', 'Less than 3 LPA'),
        ('3-6L', '3-6 LPA'),
        ('6-10L', '6-10 LPA'),
        ('10L+', 'More than 10 LPA'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #Personal Details
    address = models.CharField(max_length=255, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)

    current_skills = models.TextField(blank=True, null=True)  # comma-separated for now
    current_job = models.CharField(max_length=100, blank=True, null=True)
    current_salary = models.CharField(max_length=10, choices=SALARY_CHOICES, blank=True, null=True)

    dream_role = models.CharField(max_length=100, blank=True, null=True)
        # Resume field (optional, in case we later upload)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)

    def __str__(self):
        return self.user.username

    def age(self):
        if self.dob:
            today = date.today()
            return today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
        return None
