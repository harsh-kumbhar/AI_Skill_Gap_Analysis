from django.db import models
from django.contrib.auth.models import User
from datetime import date

class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
        
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

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    # Personal Details
    address = models.CharField(max_length=255, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)

    # Career Details
    skills = models.ManyToManyField(Skill, blank=True)
    current_job = models.CharField(max_length=100, blank=True, null=True)
    current_salary = models.CharField(max_length=10, choices=SALARY_CHOICES, blank=True, null=True)
    dream_role = models.ForeignKey("DreamRole", on_delete=models.SET_NULL, null=True, blank=True)
    profile_pic = models.ImageField(upload_to="profile_pic/", blank=True, null=True)

    # Resume field (optional, in case we later upload)
    # models.py
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)

class DreamRole(models.Model):
    name = models.CharField(max_length=100, unique=True)
    skills = models.ManyToManyField("Skill", related_name="dream_role")

    def __str__(self):
        return self.name
    
def clean(self):
    import os
    from django.core.exceptions import ValidationError
    if self.resume:
        ext = os.path.splitext(self.resume.name)[1].lower()
        if ext != ".pdf":
            raise ValidationError("Only PDF files are allowed for resume upload.")

    def __str__(self):
        return self.user.username

    @property
    def age(self):
        if self.dob:
            today = date.today()
            return today.year - self.dob.year - (
                (today.month, today.day) < (self.dob.month, self.dob.day)
            )
        return None


